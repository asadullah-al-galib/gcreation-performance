import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";
const script = readFileSync("wordpress/gcreation-performance/app.js", "utf8");
const html =
  '<main id="gcp-app"><form id="gcp-scan"><input name="url" value="https://example.com/"><button>Scan</button></form><p id="gcp-status"></p><ol id="gcp-events"></ol><section id="gcp-report"></section></main>';
const finding = {
  severity: "important",
  title: "<img src=x onerror=alert(1)>",
  affected_url: "https://example.com/",
  measured_values: { observed: 901 },
  threshold: 800,
  evidence: ["Observed server timing"],
  impact: "Performance friction",
  recommendation: "Review caching",
  steps: ["Back up", "Review caching"],
  verification_method: "Retest",
  rule_id: "slow_ttfb",
};
const report = {
  healthScore: 80,
  scoreBasis: "Measured Lighthouse score",
  incomplete: [],
  issues: [finding],
};
function setup(
  hash = "",
  handler: (path: string, body: Record<string, unknown> | null) => unknown,
) {
  const dom = new JSDOM(html, {
    url: "https://ui.example/performance-doctor/" + hash,
    runScripts: "outside-only",
  });
  Object.assign(dom.window, {
    gcpConfig: { api: "https://ui.example/api/", nonce: "test-nonce" },
    fetch: async (url: string, init: { body?: string }) => ({
      ok: true,
      json: async () =>
        handler(
          url.replace("https://ui.example/api/", ""),
          init.body ? JSON.parse(init.body) : null,
        ),
    }),
  });
  dom.window.eval(script);
  return dom;
}
test("scan UI renders actual persisted progress and safely escapes evidence", async () => {
  const calls: string[] = [];
  const dom = setup("", (path) => {
    calls.push(path);
    if (path === "scan") return { id: "test-scan" };
    if (path.startsWith("events/"))
      return [{ id: 1, type: "network.analyzed", data: { requests: 7 } }];
    if (path === "analytics") return { ok: true };
    return { state: "COMPLETED", report };
  });
  dom.window.document
    .querySelector("form")!
    .dispatchEvent(
      new dom.window.Event("submit", { bubbles: true, cancelable: true }),
    );
  await new Promise((resolve) => setTimeout(resolve, 20));
  assert.match(
    dom.window.document.querySelector("#gcp-events")!.textContent!,
    /network analyzed.*7/,
  );
  assert.match(
    dom.window.document.querySelector("#gcp-report")!.textContent!,
    /Measured Lighthouse score/,
  );
  assert.equal(
    dom.window.document.querySelectorAll("#gcp-report img").length,
    0,
  );
  assert.equal(
    dom.window.document.querySelectorAll("#gcp-report select").length,
    2,
  );
  assert.ok(calls.includes("analytics"));
  dom.window.close();
});
test("secure Fix Center removes token from URL and sends credentials in POST only", async () => {
  const calls: Record<string, unknown>[] = [];
  const token = "private-test-report-token";
  const dom = setup("#report=" + token, (_path, body) => {
    calls.push(body!);
    return { audit: { id: "paid", report }, retests: [] };
  });
  assert.equal(dom.window.location.hash, "");
  const form = dom.window.document.querySelector("#gcp-report form")!;
  const inputs = form.querySelectorAll("input");
  inputs[0].value = "42";
  inputs[1].value = "buyer@example.com";
  form.dispatchEvent(
    new dom.window.Event("submit", { bubbles: true, cancelable: true }),
  );
  await new Promise((resolve) => setTimeout(resolve, 20));
  assert.equal(calls[0].token, token);
  assert.equal(calls[0].orderId, "42");
  assert.equal(calls[0].contact, "buyer@example.com");
  assert.match(
    dom.window.document.querySelector("#gcp-report")!.textContent!,
    /Mark as Fixed/,
  );
  assert.match(
    dom.window.document.querySelector("#gcp-report")!.textContent!,
    /Test Again/,
  );
  dom.window.close();
});
