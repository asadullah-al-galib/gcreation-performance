import type { Metrics, Resource } from "../../contracts/src/index.js";
const observedSum = (resources: Resource[]) =>
  resources.length && resources.every((r) => r.bytes !== null)
    ? resources.reduce((sum, r) => sum + r.bytes!, 0)
    : resources.length
      ? null
      : 0;
export function normalize(input: {
  url: string;
  status: number | null;
  redirects: number;
  ttfbMs: number | null;
  loadMs: number | null;
  resources: Resource[];
  lighthouse?: Metrics["lighthouse"];
}): Metrics {
  const origin = new URL(input.url).origin;
  const redactUrl = (value: string) => {
    const url = new URL(value);
    url.search = "";
    url.hash = "";
    return url.href;
  };
  const resources = input.resources.map((r) => ({
    ...r,
    url: redactUrl(r.url),
    bytes:
      r.bytes !== null && Number.isFinite(r.bytes) && r.bytes >= 0
        ? r.bytes
        : null,
    durationMs:
      r.durationMs !== null &&
      Number.isFinite(r.durationMs) &&
      r.durationMs >= 0
        ? r.durationMs
        : null,
  }));
  return {
    ...input,
    resources,
    requests: resources.length,
    transferredBytes: observedSum(resources),
    jsBytes: observedSum(resources.filter((r) => r.type === "script")),
    cssBytes: observedSum(resources.filter((r) => r.type === "stylesheet")),
    imageBytes: observedSum(resources.filter((r) => r.type === "image")),
    fontBytes: observedSum(resources.filter((r) => r.type === "font")),
    thirdPartyRequests: resources.filter(
      (r) => new URL(r.url).origin !== origin,
    ).length,
    failedRequests: resources.filter(
      (r) => r.status === null || r.status >= 400,
    ).length,
    lighthouse: input.lighthouse ?? {},
  };
}
