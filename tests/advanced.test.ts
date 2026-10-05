import test from "node:test";
import assert from "node:assert/strict";
import { Store } from "../apps/audit-service/src/store.js";
import { Worker } from "../apps/audit-service/src/worker.js";
import { evaluate } from "../packages/rules/src/index.js";
import { normalize } from "../packages/metrics/src/index.js";
import { discover } from "../packages/discovery/src/index.js";
import { createApp } from "../apps/audit-service/src/server.js";
import { newToken } from "../packages/shared/src/auth.js";

const metric = normalize({
  url: "https://example.com/",
  status: 200,
  redirects: 3,
  ttfbMs: 1000,
  loadMs: 5000,
  lighthouse: { lcpMs: 4500, tbtMs: 500 },
  resources: [
    ...Array.from({ length: 105 }, (_, i) => ({
      url: `https://thirdparty.example/a${i}.js`,
      type: "script",
      status: 200,
      bytes: 30000,
      durationMs: 100,
      cacheControl: "",
      encoding: "",
      renderBlocking: i === 0,
    })),
    {
      url: "https://example.com/style.css",
      type: "stylesheet",
      status: 200,
      bytes: 250000,
      durationMs: 500,
      cacheControl: "no-cache",
      encoding: "",
    },
    {
      url: "https://example.com/image.png",
      type: "image",
      status: 200,
      bytes: 300000,
      durationMs: 500,
      mime: "image/png",
      cacheControl: "no-cache",
      encoding: "",
    },
    {
      url: "https://example.com/font.woff2",
      type: "font",
      status: 200,
      bytes: 250000,
      durationMs: 500,
      cacheControl: "no-cache",
      encoding: "",
    },
  ],
});
test("all sixteen rule families have measured fixtures and complete fix evidence", () => {
  const issues = evaluate(metric);
  const rules = new Set(issues.map((issue) => issue.rule_id));
  const failed = evaluate({
    ...metric,
    resources: [
      ...metric.resources,
      {
        url: "https://example.com/missing.js",
        type: "script",
        status: 404,
        bytes: 0,
        durationMs: 20,
      },
    ],
  });
  failed.forEach((issue) => rules.add(issue.rule_id));
  assert.equal(rules.size, 16);
  for (const issue of [...issues, ...failed]) {
    assert.ok(issue.evidence.length);
    assert.ok(Object.keys(issue.measured_values).length);
    assert.ok(issue.threshold !== undefined);
    assert.ok(issue.steps.length);
    assert.ok(issue.verification_method);
    assert.doesNotMatch(
      JSON.stringify(issue),
      /losing \d+%|increase by \d+%|Plugin .* caused/,
    );
  }
});
test("unsafe resources defer jobs with a bounded wait budget and never launch the browser", async () => {
  const store = new Store(":memory:");
  const id = store.createAudit("https://example.com/");
  let scans = 0;
  const worker = new Worker(
    store,
    async () => {
      scans++;
      return metric;
    },
    undefined,
    async () => false,
  );
  for (let i = 0; i < 11; i++) {
    store.db.prepare("UPDATE jobs SET available_at=0 WHERE audit_id=?").run(id);
    await worker.tick();
  }
  assert.equal(scans, 0);
  assert.equal(store.getAudit(id)?.state, "FAILED");
  assert.equal(
    store.db.prepare("SELECT resource_waits FROM jobs WHERE audit_id=?").get(id)
      ?.resource_waits,
    10,
  );
  store.close();
});
test("sitemap caps disclose truncation and reject cross-origin discovery", async () => {
  const fetched: string[] = [];
  const sitemap =
    "<urlset>" +
    Array.from(
      { length: 2100 },
      (_, i) => `<url><loc>https://example.com/page-${i}/</loc></url>`,
    ).join("") +
    "<url><loc>https://foreign.example/private</loc></url></urlset>";
  const result = await discover(
    "https://example.com/",
    () => {},
    async (url) => {
      fetched.push(url);
      return {
        url,
        status: 200,
        headers: { "content-type": "text/html" },
        body: new URL(url).pathname === "/" ? "<html>public</html>" : sitemap,
        redirects: 0,
        ttfbMs: 1,
      };
    },
  );
  assert.equal(result.count, 2001);
  assert.equal(result.truncated, true);
  assert.ok(
    fetched.every((url) => new URL(url).origin === "https://example.com"),
  );
  assert.ok(
    result.urls.every(
      (item) => new URL(item.url).origin === "https://example.com",
    ),
  );
});
test("custom expert review is idempotent; admin verification requires a completed retest", async () => {
  const store = new Store(":memory:");
  const secret = "strong-test-engine-secret-32-characters";
  const headers = { "x-engine-secret": secret };
  const app = createApp(store, secret);
  const id = store.createAudit("https://example.com/");
  store.claim();
  store.complete(id, {
    healthScore: null,
    scoreBasis: "unknown",
    pages: [metric],
    issues: evaluate(metric),
    incomplete: [],
    createdAt: new Date().toISOString(),
  });
  for (let i = 0; i < 2; i++)
    assert.equal(
      (
        await app.inject({
          method: "POST",
          url: "/expert/review",
          headers,
          payload: { auditId: id, contact: "owner@example.com" },
        })
      ).statusCode,
      200,
    );
  const request = store.db.prepare("SELECT * FROM expert_requests").get()!;
  assert.equal(
    store.db.prepare("SELECT count(*) AS n FROM expert_requests").get()?.n,
    1,
  );
  assert.notEqual(request.contact_hash, "owner@example.com");
  assert.equal(
    (
      await app.inject({
        method: "PATCH",
        url: "/admin/experts/" + request.id,
        headers,
        payload: { kind: "review", state: "Verified" },
      })
    ).statusCode,
    409,
  );
  assert.equal(
    (
      await app.inject({
        method: "PATCH",
        url: "/admin/experts/" + request.id,
        headers,
        payload: { kind: "review", state: "In Review" },
      })
    ).statusCode,
    200,
  );
  await app.close();
  store.close();
});
test("paid retest is restricted to previously audited pages and exposes measured before/after", async () => {
  const store = new Store(":memory:");
  const secret = "strong-test-engine-secret-32-characters";
  const headers = { "x-engine-secret": secret };
  const app = createApp(store, secret);
  const id = store.createAudit("https://example.com/");
  store.claim();
  store.saveInventory(id, {
    urls: [{ url: "https://example.com/", kind: "homepage" }],
    count: 1,
    truncated: false,
    sitemaps: [],
    wordpress: false,
    woocommerce: false,
  });
  store.complete(id, {
    healthScore: 20,
    scoreBasis: "controlled fixture",
    pages: [metric],
    issues: evaluate(metric),
    incomplete: [],
    createdAt: new Date().toISOString(),
  });
  const token = newToken();
  const credentials = { orderId: "55", contact: "owner@example.com", token };
  const paid = await app.inject({
    method: "POST",
    url: "/orders/paid",
    headers,
    payload: {
      wcOrderId: "55",
      auditId: id,
      scope: "major5",
      mode: "self",
      contact: credentials.contact,
      reportToken: token,
      amount: 499,
      currency: "BDT",
    },
  });
  const paidId = paid.json().auditId;
  store.claim();
  store.complete(paidId, {
    healthScore: 20,
    scoreBasis: "controlled fixture",
    pages: [metric],
    issues: evaluate(metric),
    incomplete: [],
    createdAt: new Date().toISOString(),
  });
  assert.equal(
    (
      await app.inject({
        method: "POST",
        url: "/reports/access",
        headers,
        payload: {
          ...credentials,
          action: "retest",
          url: "https://other.example/",
        },
      })
    ).statusCode,
    400,
  );
  const retest = await app.inject({
    method: "POST",
    url: "/reports/access",
    headers,
    payload: { ...credentials, action: "retest", url: metric.url },
  });
  assert.equal(retest.statusCode, 200);
  const duplicate = await app.inject({
    method: "POST",
    url: "/reports/access",
    headers,
    payload: { ...credentials, action: "retest", url: metric.url },
  });
  assert.equal(duplicate.json().auditId, retest.json().auditId);
  assert.equal(duplicate.json().idempotent, true);
  store.claim();
  store.complete(retest.json().auditId, {
    healthScore: 90,
    scoreBasis: "controlled fixture",
    pages: [{ ...metric, ttfbMs: 400 }],
    issues: [],
    incomplete: [],
    createdAt: new Date().toISOString(),
  });
  const report = await app.inject({
    method: "POST",
    url: "/reports/access",
    headers,
    payload: credentials,
  });
  assert.equal(report.json().retests[0].comparison[0].ttfbBefore, 1000);
  assert.equal(report.json().retests[0].comparison[0].ttfbAfter, 400);
  await app.close();
  store.close();
});

test("persistent free admission quotas and concurrent API submissions remain bounded", async () => {
  const store = new Store(":memory:");
  const secret = "strong-test-engine-secret-32-characters";
  const app = createApp(store, secret);
  const requests = await Promise.all(
    Array.from({ length: 12 }, () =>
      app.inject({
        method: "POST",
        url: "/audits",
        headers: { "x-engine-secret": secret, "x-client-key": "a".repeat(64) },
        payload: { url: "https://8.8.8.8/" },
      }),
    ),
  );
  assert.equal(requests.filter((reply) => reply.statusCode === 202).length, 5);
  assert.equal(requests.filter((reply) => reply.statusCode === 429).length, 7);
  assert.equal(store.db.prepare("SELECT count(*) AS n FROM jobs").get()?.n, 5);
  for (let i = 0; i < 45; i++) store.createAudit("https://example.com/");
  assert.equal(
    (
      await app.inject({
        method: "POST",
        url: "/audits",
        headers: { "x-engine-secret": secret, "x-client-key": "b".repeat(64) },
        payload: { url: "https://8.8.8.8/" },
      })
    ).statusCode,
    429,
  );
  assert.equal(store.db.prepare("SELECT count(*) AS n FROM jobs").get()?.n, 50);
  await app.close();
  store.close();
});
