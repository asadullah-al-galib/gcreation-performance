import { readFile } from "node:fs/promises";
import type { Emit, Metrics } from "../../../packages/contracts/src/index.js";
import {
  discover,
  selectPages,
} from "../../../packages/discovery/src/index.js";
import { safeFetch } from "../../../packages/shared/src/security.js";
import { scanPage } from "../../../packages/scanner/src/index.js";
import { createReport } from "../../../packages/report-engine/src/index.js";
import type { Store } from "./store.js";
async function cgroupMeasurements() {
  const cpu = await readFile("/sys/fs/cgroup/cpu.stat", "utf8").catch(() => "");
  const memory = await readFile("/sys/fs/cgroup/memory.current", "utf8").catch(
    () => "",
  );
  return {
    cpuUsec: /usage_usec\s+(\d+)/.test(cpu)
      ? Number(/usage_usec\s+(\d+)/.exec(cpu)![1])
      : null,
    memoryBytes: /^\d+\s*$/.test(memory) ? Number(memory) : null,
  };
}
export async function resourceSafe() {
  try {
    const mem = await readFile("/proc/meminfo", "utf8");
    const available = Number(/MemAvailable:\s+(\d+)/.exec(mem)?.[1] ?? 0);
    const pressure = await readFile("/proc/pressure/memory", "utf8").catch(
      () => "some avg10=0",
    );
    const avg = Number(/some avg10=([\d.]+)/.exec(pressure)?.[1] ?? 100);
    return (
      available > Number(process.env.MIN_AVAILABLE_KB ?? 1200000) &&
      avg < Number(process.env.MAX_MEMORY_PRESSURE ?? 10)
    );
  } catch {
    return false;
  }
}
export class Worker {
  busy = false;
  stopped = false;
  constructor(
    private store: Store,
    private scan = scanPage,
    private discoverSite = discover,
    private resources = resourceSafe,
  ) {}
  async tick() {
    if (this.busy || this.stopped) return;
    this.busy = true;
    const audit = this.store.claim();
    if (!audit) {
      this.busy = false;
      return;
    }
    const controller = new AbortController();
    const deadline = setTimeout(
      () => controller.abort(),
      audit.scope === "full"
        ? 900000
        : audit.scope === "major5"
          ? 480000
          : 240000,
    );
    const started = performance.now();
    const before = await cgroupMeasurements();
    let peak = before.memoryBytes;
    const sample = setInterval(() => {
      void cgroupMeasurements().then((value) => {
        if (value.memoryBytes !== null)
          peak = Math.max(peak ?? 0, value.memoryBytes);
      });
    }, 1000);
    const emit: Emit = (type, data = {}) =>
      this.store.emit(audit.id, type, data);
    try {
      if (!(await this.resources())) {
        this.store.wait(audit.id);
        return;
      }
      const inventory =
        audit.scope === "retest"
          ? {
              urls: [{ url: audit.url, kind: "page" }],
              count: 1,
              truncated: false,
              sitemaps: [],
              wordpress: false,
              woocommerce: false,
            }
          : await this.discoverSite(audit.url, emit);
      this.store.saveInventory(audit.id, inventory);
      const incomplete: string[] = [];
      if (inventory.truncated)
        incomplete.push("Discovery is bounded; inventory may be incomplete.");
      if (audit.scope === "full")
        for (const item of inventory.urls) {
          if (controller.signal.aborted)
            throw new Error("Overall audit deadline exceeded");
          const response = await safeFetch(item.url, {
            method: "HEAD",
            maxBytes: 1024,
          }).catch(() => null);
          this.store.emit(audit.id, "url.validated", {
            url: item.url,
            status: response?.status ?? null,
            kind: item.kind,
          });
        }
      const pages: Metrics[] = [];
      const start = Date.now();
      for (const [index, item] of selectPages(
        inventory,
        audit.scope,
      ).entries()) {
        if (controller.signal.aborted || Date.now() - start > 720000)
          throw new Error("Audit time budget exceeded");
        const stage =
          index === 0
            ? "homepage"
            : item.kind === "product"
              ? "product"
              : "page";
        if (stage === "product") emit("product.discovered", { url: item.url });
        emit(`${stage}.started`, { url: item.url });
        pages.push(
          await this.scan(item.url, index === 0, emit, controller.signal),
        );
        emit(`${stage}.completed`, { url: item.url });
      }
      emit("rules.started", {});
      const report = createReport(pages, incomplete);
      emit("rules.completed", { count: report.issues.length });
      this.store.complete(audit.id, report);
    } catch {
      this.store.fail(
        audit.id,
        "Audit could not complete safely. Retry or request expert review.",
      );
    } finally {
      clearTimeout(deadline);
      clearInterval(sample);
      const after = await cgroupMeasurements();
      this.store.analytics(audit.id, "scanner.resources", {
        wallMs: performance.now() - started,
        cgroupCpuUsec:
          before.cpuUsec !== null && after.cpuUsec !== null
            ? after.cpuUsec - before.cpuUsec
            : null,
        sampledCgroupPeakMemoryBytes: peak,
        basis:
          "Audit container cgroup including Node and Chromium when available; null means unavailable",
      });
      this.busy = false;
    }
  }
}
