import { explanations } from "./recommendations.js";
import type { Issue, Metrics } from "../../contracts/src/index.js";
export const thresholds = {
  ttfbMs: 800,
  lcpMs: 2500,
  tbtMs: 200,
  requests: 100,
  pageBytes: 3_000_000,
  jsBytes: 500_000,
  cssBytes: 200_000,
  imageBytes: 250_000,
  thirdParty: 20,
  fontBytes: 200_000,
  redirects: 1,
};
export function evaluate(metrics: Metrics): Issue[] {
  const issues: Issue[] = [];
  const add = (
    id: string,
    category: string,
    title: string,
    value: number | string,
    threshold: number | string,
    evidence: string[],
    recommendation: string,
    severity: Issue["severity"] = "important",
  ) =>
    issues.push({
      rule_id: id,
      category,
      severity,
      title,
      affected_url: metrics.url,
      evidence,
      measured_values: { observed: value },
      threshold,
      impact:
        "This can add performance friction for visitors. Impact depends on the page and device.",
      recommendation,
      steps: explanations.steps(id),
      verification_method:
        "Run a fresh audit of the affected URL and compare the observed metric with this evidence.",
    });
  const numeric: [
    string,
    string,
    string,
    number | null | undefined,
    number,
    string,
  ][] = [
    [
      "slow_ttfb",
      "server",
      "Slow server response",
      metrics.ttfbMs,
      thresholds.ttfbMs,
      "Review page caching and hosting response time; deeper WordPress inspection may be required.",
    ],
    [
      "poor_lcp",
      "rendering",
      "Largest content appears late",
      metrics.lighthouse.lcpMs,
      thresholds.lcpMs,
      "Prioritize the main visible image and reduce work before it renders.",
    ],
    [
      "high_blocking",
      "javascript",
      "High main-thread blocking time",
      metrics.lighthouse.tbtMs,
      thresholds.tbtMs,
      "Reduce unnecessary JavaScript and defer optional features.",
    ],
    [
      "excessive_requests",
      "network",
      "Many resource requests",
      metrics.requests,
      thresholds.requests,
      "Remove unused resources and consolidate only where measurement supports it.",
    ],
    [
      "page_weight",
      "network",
      "Large transferred page payload",
      metrics.transferredBytes,
      thresholds.pageBytes,
      "Reduce the largest measured image, script and font payloads.",
    ],
    [
      "javascript_payload",
      "javascript",
      "Large JavaScript payload",
      metrics.jsBytes,
      thresholds.jsBytes,
      "Remove unused scripts and load optional scripts after interaction.",
    ],
    [
      "css_payload",
      "css",
      "Large CSS payload",
      metrics.cssBytes,
      thresholds.cssBytes,
      "Remove unused styles and review theme-generated CSS.",
    ],
    [
      "third_party",
      "network",
      "Many third-party requests",
      metrics.thirdPartyRequests,
      thresholds.thirdParty,
      "Review each third-party feature and delay optional integrations.",
    ],
    [
      "font_overhead",
      "fonts",
      "Large font payload",
      metrics.fontBytes,
      thresholds.fontBytes,
      "Limit font families, weights and character ranges.",
    ],
    [
      "redirect_chain",
      "network",
      "Navigation redirect chain",
      metrics.redirects,
      thresholds.redirects,
      "Link directly to the final canonical URL.",
    ],
  ];
  for (const [id, category, title, value, threshold, action] of numeric)
    if (typeof value === "number" && value > threshold)
      add(
        id,
        category,
        title,
        value,
        threshold,
        [`Observed ${value}; threshold ${threshold}`],
        action,
        id === "poor_lcp" && value > 4000 ? "critical" : "important",
      );
  const resources = metrics.resources;
  const resourceRule = (
    id: string,
    category: string,
    title: string,
    affected: typeof resources,
    threshold: number | string,
    action: string,
  ) => {
    if (affected.length)
      add(
        id,
        category,
        title,
        affected.length,
        threshold,
        affected
          .slice(0, 10)
          .map(
            (r) =>
              `${r.url}: status=${r.status ?? "failed"}, bytes=${r.bytes ?? "not observed"}`,
          ),
        action,
      );
  };
  resourceRule(
    "oversized_images",
    "images",
    "Large image resources",
    resources.filter(
      (r) =>
        r.type === "image" &&
        r.bytes !== null &&
        r.bytes > thresholds.imageBytes,
    ),
    thresholds.imageBytes,
    "Resize and compress the listed images for their rendered dimensions.",
  );
  resourceRule(
    "modern_images",
    "images",
    "Modern image format opportunity",
    resources.filter(
      (r) =>
        r.type === "image" &&
        /image\/(jpeg|png)/.test(r.mime ?? "") &&
        r.bytes !== null &&
        r.bytes > 100_000,
    ),
    100_000,
    "Compare WebP or AVIF output while preserving visible quality.",
  );
  resourceRule(
    "render_blocking",
    "rendering",
    "Render-blocking resources observed",
    resources.filter((r) => r.renderBlocking === true),
    "observed render blocking",
    "Review critical styles and defer optional blocking scripts.",
  );
  resourceRule(
    "failed_resources",
    "network",
    "Resource requests failed",
    resources.filter((r) => r.status === null || r.status >= 400),
    0,
    "Correct the listed resource URLs and inspect access or server errors.",
  );
  const staticResources = resources.filter(
    (r) =>
      ["script", "stylesheet", "image", "font"].includes(r.type) &&
      r.status === 200,
  );
  resourceRule(
    "cache_policy",
    "cache",
    "Static resources may not be reusable from cache",
    staticResources.filter(
      (r) =>
        r.cacheControl !== undefined &&
        !/max-age=[1-9]\d*|immutable/i.test(r.cacheControl),
    ),
    "cache lifetime absent or zero",
    "Set suitable cache lifetimes for versioned public static resources; do not cache private pages.",
  );
  resourceRule(
    "compression",
    "network",
    "Text compression opportunity",
    staticResources.filter(
      (r) =>
        ["script", "stylesheet"].includes(r.type) &&
        r.bytes !== null &&
        r.bytes > 20_000 &&
        r.encoding !== undefined &&
        !/gzip|br|zstd/.test(r.encoding),
    ),
    20_000,
    "Enable supported text compression for the listed resources.",
  );
  return issues;
}
