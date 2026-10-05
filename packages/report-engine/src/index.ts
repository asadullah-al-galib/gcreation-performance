import type { Metrics, Report } from "../../contracts/src/index.js";
import { evaluate } from "../../rules/src/index.js";
export function createReport(
  pages: Metrics[],
  incomplete: string[] = [],
): Report {
  const scores = pages
    .map((p) => p.lighthouse.performanceScore)
    .filter((n): n is number => typeof n === "number");
  return {
    healthScore: scores.length
      ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
      : null,
    scoreBasis:
      "Observed Lighthouse performance scores for selected pages; lab measurement, not revenue prediction.",
    pages,
    issues: pages
      .flatMap(evaluate)
      .sort(
        (a, b) =>
          ["critical", "important", "opportunity"].indexOf(a.severity) -
          ["critical", "important", "opportunity"].indexOf(b.severity),
      ),
    incomplete,
    createdAt: new Date().toISOString(),
  };
}
export function compare(before: Report, after: Report) {
  return after.pages.map((page) => {
    const previous = before.pages.find((p) => p.url === page.url);
    return {
      url: page.url,
      before: previous?.lighthouse ?? null,
      after: page.lighthouse,
      ttfbBefore: previous?.ttfbMs ?? null,
      ttfbAfter: page.ttfbMs,
    };
  });
}
