import test from "node:test";
import assert from "node:assert/strict";
import { Store } from "../apps/audit-service/src/store.js";
import { createApp } from "../apps/audit-service/src/server.js";
import { Worker } from "../apps/audit-service/src/worker.js";
import { normalize } from "../packages/metrics/src/index.js";
import { newToken } from "../packages/shared/src/auth.js";
import { mkdtempSync, rmSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const secret = "test-secret-that-is-at-least-32-characters";
const headers = { "x-engine-secret": secret };
const inventory = {
  urls: [
    { url: "https://example.com/", kind: "homepage" },
    { url: "https://example.com/product/demo/", kind: "product" },
  ],
  count: 2,
  truncated: false,
  sitemaps: ["https://example.com/sitemap.xml"],
  wordpress: true,
  woocommerce: true,
};

test("health public, management protected, scan SSRF rejected", async () => {
  const store = new Store(":memory:");
  const app = createApp(store, secret);
  assert.equal((await app.inject("/health")).statusCode, 200);
  assert.equal((await app.inject("/admin/summary")).statusCode, 401);
  for (const url of [
    "http://localhost/",
    "http://127.0.0.1/",
    "http://10.1.1.1/",
    "file:///etc/passwd",
  ])
    assert.equal(
      (
        await app.inject({
          method: "POST",
          url: "/audits",
          headers,
          payload: { url },
        })
      ).statusCode,
      422,
    );
  await app.close();
  store.close();
});
test("worker lifecycle, real events, pricing, idempotent payment and secure Fix Center", async () => {
  const store = new Store(":memory:");
  const app = createApp(store, secret);
  const id = store.createAudit("https://example.com/");
  let scans = 0;
  let simultaneous = 0;
  let max = 0;
  const worker = new Worker(
    store,
    async (url, _lh, emit) => {
      simultaneous++;
      max = Math.max(max, simultaneous);
      scans++;
      emit("network.analyzed", { requests: 0 });
      await new Promise((resolve) => setTimeout(resolve, 5));
      simultaneous--;
      return normalize({
        url,
        status: 200,
        redirects: 0,
        ttfbMs: 900,
        loadMs: 50,
        resources: [],
        lighthouse: { performanceScore: 80 },
      });
    },
    async () => inventory,
    async () => true,
  );
  await Promise.all([worker.tick(), worker.tick()]);
  assert.equal(max, 1);
  assert.equal(scans, 2);
  assert.equal(store.getAudit(id)?.state, "COMPLETED");
  const events = await app.inject({ url: `/audits/${id}/events`, headers });
  assert.ok(
    events
      .json()
      .some((event: { type: string }) => event.type === "report.ready"),
  );
  const stream = await app.inject({ url: `/audits/${id}/stream`, headers });
  assert.equal(stream.headers["content-type"], "text/event-stream");
  assert.match(stream.body, /event: report.ready/);
  const quote = await app.inject({
    method: "POST",
    url: "/quotes",
    headers,
    payload: { auditId: id, scope: "major5", mode: "self", amount: 1 },
  });
  assert.equal(quote.json().amount, 499);
  const token = newToken();
  const order = {
    wcOrderId: "42",
    auditId: id,
    scope: "major5",
    mode: "self",
    contact: "buyer@example.com",
    reportToken: token,
    amount: 499,
    currency: "BDT",
  };
  assert.equal(
    (
      await app.inject({
        method: "POST",
        url: "/orders/paid",
        headers,
        payload: { ...order, amount: 1 },
      })
    ).statusCode,
    409,
  );
  const first = await app.inject({
    method: "POST",
    url: "/orders/paid",
    headers,
    payload: order,
  });
  assert.equal(first.statusCode, 201);
  const duplicate = await app.inject({
    method: "POST",
    url: "/orders/paid",
    headers,
    payload: order,
  });
  assert.equal(duplicate.json().auditId, first.json().auditId);
  assert.equal(
    store.db.prepare("SELECT count(*) AS n FROM orders").get()?.n,
    1,
  );
  await worker.tick();
  assert.equal(
    (await app.inject({ url: "/audits/" + first.json().auditId, headers }))
      .statusCode,
    403,
  );
  const credentials = { orderId: "42", contact: "buyer@example.com", token };
  assert.equal(
    (
      await app.inject({
        method: "POST",
        url: "/reports/access",
        headers,
        payload: { ...credentials, token: newToken() },
      })
    ).statusCode,
    403,
  );
  const access = await app.inject({
    method: "POST",
    url: "/reports/access",
    headers,
    payload: credentials,
  });
  assert.equal(access.statusCode, 200);
  assert.ok(access.json().audit.report.issues.length);
  const fixed = await app.inject({
    method: "POST",
    url: "/reports/access",
    headers,
    payload: {
      ...credentials,
      action: "fixed",
      ruleId: "slow_ttfb",
      url: "https://example.com/",
    },
  });
  assert.equal(fixed.json().verified, false);
  for (let i = 0; i < 2; i++)
    assert.equal(
      (
        await app.inject({
          method: "POST",
          url: "/reports/access",
          headers,
          payload: { ...credentials, action: "expert" },
        })
      ).json().state,
      "Pending",
    );
  assert.equal(
    store.db.prepare("SELECT count(*) AS n FROM expert_tasks").get()?.n,
    1,
  );
  await app.close();
  store.close();
});
test("SQLite lifecycle survives reopening and stale running job fails visibly", () => {
  mkdirSync(join(process.cwd(), ".ops/test-artifacts"), { recursive: true });
  const directory = mkdtempSync(
    join(process.cwd(), ".ops/test-artifacts/sqlite-"),
  );
  const path = join(directory, "audit.sqlite");
  let store = new Store(path);
  const id = store.createAudit("https://example.com/");
  store.claim();
  store.close();
  store = new Store(path);
  store.recover();
  assert.equal(store.getAudit(id)?.state, "FAILED");
  store.close();
  rmSync(directory, { recursive: true });
});
