import test from "node:test";
import assert from "node:assert/strict";
import {
  parsePublicUrl,
  isPublicIp,
  validateTarget,
  SecurityError,
} from "../packages/shared/src/security.js";
import { quote } from "../packages/shared/src/pricing.js";
import {
  newToken,
  hashToken,
  reportAuthorized,
} from "../packages/shared/src/auth.js";
import { normalize } from "../packages/metrics/src/index.js";
import { evaluate, thresholds } from "../packages/rules/src/index.js";
import { Store } from "../apps/audit-service/src/store.js";
import {
  discover,
  selectPages,
  classify,
} from "../packages/discovery/src/index.js";
import type { SafeResponse } from "../packages/shared/src/security.js";

test("URL schemes, internal hosts, credentials and ports are rejected", () => {
  for (const url of [
    "file:///etc/passwd",
    "ftp://example.com",
    "http://localhost",
    "http://db",
    "http://host.local",
    "http://user:pass@example.com",
    "http://example.com:3101",
    "http://performance.gcreation.agency",
    "http://dev.gcreation.agency",
  ])
    assert.throws(() => parsePublicUrl(url), SecurityError);
  assert.equal(
    parsePublicUrl("https://EXAMPLE.com/").href,
    "https://example.com/",
  );
});
test("private, reserved, metadata and mapped IPv6 are blocked", () => {
  for (const ip of [
    "127.0.0.1",
    "10.0.0.1",
    "172.16.0.1",
    "192.168.1.1",
    "169.254.169.254",
    "0.0.0.0",
    "100.64.1.1",
    "192.0.2.1",
    "::1",
    "fc00::1",
    "fe80::1",
    "::ffff:8.8.8.8",
    "2002:0808:0808::1",
  ])
    assert.equal(isPublicIp(ip), false, ip);
  for (const ip of ["8.8.8.8", "1.1.1.1", "2606:4700:4700::1111"])
    assert.equal(isPublicIp(ip), true, ip);
});
test("every DNS answer and redirect destination is revalidated", async () => {
  await assert.rejects(
    validateTarget("https://example.com", async () => [
      { address: "8.8.8.8", family: 4 },
      { address: "127.0.0.1", family: 4 },
    ]),
    SecurityError,
  );
  await assert.rejects(
    validateTarget(
      new URL("http://169.254.169.254/latest", "https://example.com").href,
    ),
    SecurityError,
  );
  let calls = 0;
  const rebinding = async () => [
    { address: ++calls === 1 ? "8.8.8.8" : "10.0.0.1", family: 4 },
  ];
  await validateTarget("https://example.com", rebinding);
  await assert.rejects(
    validateTarget("https://example.com", rebinding),
    SecurityError,
  );
});
test("trusted pricing exact boundaries and custom review", () => {
  assert.equal(quote("major5", 300, "self").amount, 499);
  for (const [count, price] of [
    [1, 699],
    [25, 699],
    [26, 999],
    [100, 999],
    [101, 1499],
    [500, 1499],
    [501, 2499],
    [2000, 2499],
  ])
    assert.equal(quote("full", count, "expert").amount, price);
  assert.equal(quote("full", 2001, "self").amount, null);
  assert.throws(() => quote("full", 0, "self"));
});
test("report tokens require token/order/contact and do not grant access by ID", () => {
  const token = newToken();
  const hash = hashToken(token);
  assert.equal(
    reportAuthorized(
      token,
      hash,
      "12",
      "12",
      "CLIENT@EXAMPLE.COM",
      hashToken("client@example.com"),
    ),
    true,
  );
  assert.equal(
    reportAuthorized(
      newToken(),
      hash,
      "12",
      "12",
      "client@example.com",
      hashToken("client@example.com"),
    ),
    false,
  );
  assert.equal(
    reportAuthorized(
      token,
      hash,
      "13",
      "12",
      "client@example.com",
      hashToken("client@example.com"),
    ),
    false,
  );
});
test("unknown byte measurements stay unknown and rules use thresholds", () => {
  const metric = normalize({
    url: "https://example.com/",
    status: 200,
    redirects: 0,
    ttfbMs: thresholds.ttfbMs,
    loadMs: null,
    resources: [
      {
        url: "https://example.com/a.js",
        type: "script",
        bytes: null,
        status: 200,
        durationMs: null,
      },
    ],
  });
  assert.equal(metric.transferredBytes, null);
  assert.equal(metric.jsBytes, null);
  assert.equal(evaluate(metric).length, 0);
  metric.ttfbMs = thresholds.ttfbMs + 1;
  const issues = evaluate(metric);
  assert.equal(issues[0].rule_id, "slow_ttfb");
  assert.ok(issues[0].evidence.length);
});
test("SQLite migrations, persisted lifecycle and single worker claim", () => {
  const store = new Store(":memory:");
  const id = store.createAudit("https://example.com/");
  const paid = store.createAudit("https://example.org/", "major5");
  assert.equal(store.claim()?.id, paid);
  assert.equal(store.claim(), null);
  store.complete(paid, {
    healthScore: null,
    scoreBasis: "unavailable",
    pages: [],
    issues: [],
    incomplete: [],
    createdAt: new Date().toISOString(),
  });
  assert.equal(store.claim()?.id, id);
  store.wait(id);
  assert.equal(store.getAudit(id)?.state, "WAITING_FOR_RESOURCES");
  store.db.prepare("UPDATE jobs SET available_at=0 WHERE audit_id=?").run(id);
  assert.equal(store.claim()?.id, id);
  store.fail(id, "controlled failure");
  assert.equal(store.getAudit(id)?.state, "FAILED");
  assert.equal(store.claim(), null);
  assert.equal(
    store.db.prepare("SELECT count(*) AS n FROM migrations").get()?.n,
    4,
  );
  store.close();
});
test("sitemap index discovery, platform detection and representative products", async () => {
  const pages: Record<string, string> = {
    "/": '<html>wp-content woocommerce <a href="/about/">About</a></html>',
    "/sitemap.xml":
      "<sitemapindex><sitemap><loc>https://example.com/products.xml</loc></sitemap></sitemapindex>",
    "/products.xml":
      "<urlset><url><loc>https://example.com/product/demo/</loc></url><url><loc>https://evil.example/product/a</loc></url></urlset>",
  };
  const events: string[] = [];
  const result = await discover(
    "https://example.com/",
    (event) => events.push(event),
    async (url): Promise<SafeResponse> => ({
      url,
      status: pages[new URL(url).pathname] ? 200 : 404,
      headers: { "content-type": "text/html" },
      body: pages[new URL(url).pathname] ?? "",
      redirects: 0,
      ttfbMs: 4,
    }),
  );
  assert.equal(result.count, 3);
  assert.equal(result.woocommerce, true);
  assert.equal(result.wordpress, true);
  assert.ok(events.includes("sitemap.discovered"));
  assert.equal(selectPages(result, "free")[1].kind, "product");
  assert.equal(classify("https://example.com/checkout/"), "checkout");
});
