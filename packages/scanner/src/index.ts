import { chromium } from "playwright";
import lighthouse from "lighthouse";
import type { Emit, Metrics, Resource } from "../../contracts/src/index.js";
import { normalize } from "../../metrics/src/index.js";
import { validateTarget } from "../../shared/src/security.js";

export async function scanPage(
  url: string,
  withLighthouse: boolean,
  emit: Emit,
  signal?: AbortSignal,
): Promise<Metrics> {
  if (!process.env.BROWSER_PROXY)
    throw new Error("Validated browser egress proxy is required");
  await validateTarget(url);
  const browser = await chromium.launch({
    headless: true,
    chromiumSandbox: true,
    proxy: { server: process.env.BROWSER_PROXY, bypass: "<-loopback>" },
    args: [
      "--disable-quic",
      "--force-webrtc-ip-handling-policy=disable_non_proxied_udp",
      "--remote-debugging-port=9222",
    ],
    timeout: 30000,
  });
  const deadline = setTimeout(() => void browser.close(), 90000);
  const abort = () => {
    void browser.close();
  };
  signal?.addEventListener("abort", abort, { once: true });
  if (signal?.aborted) abort();
  try {
    const context = await browser.newContext({
      serviceWorkers: "block",
      acceptDownloads: false,
      viewport: { width: 1365, height: 768 },
    });
    const page = await context.newPage();
    const resources: Resource[] = [];
    let requests = 0;
    let bytes = 0;
    await context.route("**/*", async (route) => {
      try {
        if (++requests > 250) {
          await page.close();
          throw new Error("Request limit");
        }
        const request = route.request();
        if (!["GET", "HEAD"].includes(request.method()))
          throw new Error("Read-only scan");
        let redirects = 0;
        for (
          let prior = request.redirectedFrom();
          prior;
          prior = prior.redirectedFrom()
        )
          redirects++;
        if (redirects > 5) throw new Error("Redirect limit");
        await validateTarget(request.url());
        await route.continue();
      } catch {
        await route.abort("blockedbyclient").catch(() => {});
      }
    });
    page.on("download", (download) => void download.cancel());
    await context.routeWebSocket("**/*", (socket) => socket.close());
    const pending: Promise<void>[] = [];
    page.on("requestfinished", (request) => {
      pending.push(
        (async () => {
          const response = await request.response();
          const sizes = await request.sizes().catch(() => null);
          const timing = request.timing();
          const headers = response ? await response.allHeaders() : {};
          const size = sizes
            ? sizes.responseBodySize + sizes.responseHeadersSize
            : null;
          bytes += size ?? 0;
          if (bytes > 50 * 1024 * 1024) await page.close();
          resources.push({
            url: request.url(),
            type: request.resourceType(),
            status: response?.status() ?? null,
            bytes: size,
            durationMs: timing.responseEnd >= 0 ? timing.responseEnd : null,
            cacheControl: headers["cache-control"] ?? "",
            encoding: headers["content-encoding"] ?? "",
            mime: headers["content-type"] ?? "",
          });
        })().catch(() => {}),
      );
    });
    page.on("requestfailed", (request) => {
      if (resources.length < 250)
        resources.push({
          url: request.url(),
          type: request.resourceType(),
          status: null,
          bytes: null,
          durationMs: null,
        });
    });
    const response = await page.goto(url, {
      waitUntil: "load",
      timeout: 30000,
    });
    await page.waitForTimeout(1000);
    await Promise.all(pending);
    const timing = await page.evaluate(() => {
      const nav = performance.getEntriesByType("navigation")[0] as
        | PerformanceNavigationTiming
        | undefined;
      return nav
        ? {
            ttfbMs: nav.responseStart - nav.requestStart,
            loadMs: nav.loadEventEnd,
            redirects: nav.redirectCount,
          }
        : null;
    });
    const blocking = await page.evaluate(() =>
      performance.getEntriesByType("resource").map((entry) => {
        const resource = entry as PerformanceResourceTiming & {
          renderBlockingStatus?: string;
        };
        return {
          url: resource.name,
          status: resource.renderBlockingStatus ?? null,
        };
      }),
    );
    for (const resource of resources) {
      const observed = blocking.find((item) => item.url === resource.url);
      if (observed?.status !== null && observed?.status !== undefined)
        resource.renderBlocking = observed.status === "blocking";
    }
    emit("resources.discovered", { count: resources.length });
    emit("images.analyzed", {
      count: resources.filter((r) => r.type === "image").length,
    });
    emit("network.analyzed", { requests: resources.length });
    emit("server.analyzed", { ttfbMs: timing?.ttfbMs ?? null });
    let observedRedirects = 0;
    for (
      let prior = response?.request().redirectedFrom();
      prior;
      prior = prior.redirectedFrom()
    )
      observedRedirects++;
    const metrics = normalize({
      url,
      status: response?.status() ?? null,
      redirects: observedRedirects,
      ttfbMs: timing?.ttfbMs ?? null,
      loadMs: timing?.loadMs ?? null,
      resources,
    });
    await context.close();
    if (withLighthouse) {
      emit("lighthouse.started", {});
      const result = await lighthouse(url, {
        port: 9222,
        onlyCategories: ["performance"],
        output: "json",
        logLevel: "error",
        maxWaitForLoad: 30000,
      });
      if (!result || result.lhr.runtimeError)
        throw new Error("Lighthouse did not complete reliably");
      const audits = result.lhr.audits;
      for (const [key, id] of Object.entries({
        lcpMs: "largest-contentful-paint",
        cls: "cumulative-layout-shift",
        fcpMs: "first-contentful-paint",
        tbtMs: "total-blocking-time",
        speedIndexMs: "speed-index",
      })) {
        const value = audits[id]?.numericValue;
        if (typeof value === "number" && Number.isFinite(value))
          metrics.lighthouse[key as keyof Metrics["lighthouse"]] = value;
      }
      const score = result.lhr.categories.performance.score;
      if (typeof score === "number")
        metrics.lighthouse.performanceScore = Math.round(score * 100);
      emit("lighthouse.completed", { metrics: metrics.lighthouse });
    }
    return metrics;
  } finally {
    clearTimeout(deadline);
    signal?.removeEventListener("abort", abort);
    await browser.close();
  }
}
