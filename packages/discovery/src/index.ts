import type { Emit, Inventory, Scope } from "../../contracts/src/index.js";
import { safeFetch, type SafeResponse } from "../../shared/src/security.js";
export type Fetcher = (url: string) => Promise<SafeResponse>;
export function classify(input: string): string {
  const path = new URL(input).pathname.toLowerCase();
  if (path === "/") return "homepage";
  if (/\/(cart|checkout|my-account|account)(\/|$)/.test(path))
    return path.includes("checkout")
      ? "checkout"
      : path.includes("cart")
        ? "cart"
        : "account";
  if (/\/(product|products)\//.test(path)) return "product";
  if (/\/product-category\//.test(path)) return "product category";
  if (/\/(blog|news)\//.test(path)) return "blog post";
  if (/\/category\//.test(path)) return "category";
  if (new URL(input).searchParams.has("s")) return "search";
  return "page";
}
function candidates(body: string, pattern: RegExp) {
  return [...body.matchAll(pattern)].map((match) =>
    match[1].replace(/&amp;/g, "&").trim(),
  );
}
export async function discover(
  input: string,
  emit: Emit,
  fetcher: Fetcher = safeFetch,
): Promise<Inventory> {
  const home = await fetcher(input);
  if (
    home.status < 200 ||
    home.status >= 400 ||
    !/text\/html/i.test(home.headers["content-type"] ?? "")
  )
    throw new Error("Homepage is not reachable HTML");
  emit("site.connected", { status: home.status });
  const origin = new URL(home.url).origin;
  const wordpress = /wp-content|wp-includes|api\.w\.org/i.test(
    home.body + JSON.stringify(home.headers),
  );
  const woocommerce = /woocommerce|wc-block|wc-add-to-cart/i.test(home.body);
  emit("platform.detected", { wordpress, woocommerce });
  const urls = new Set<string>([new URL("/", origin).href]);
  const add = (candidate: string) => {
    try {
      const url = new URL(candidate, home.url);
      url.hash = "";
      if (
        url.origin === origin &&
        !url.username &&
        !url.password &&
        !/\.(pdf|png|jpe?g|webp|css|js|zip|xml)$/i.test(url.pathname) &&
        !url.search &&
        urls.size < 2001
      )
        urls.add(url.href);
    } catch {
      /* malformed remote link */
    }
  };
  for (const link of candidates(home.body, /(?:href)\s*=\s*["']([^"']+)["']/gi))
    add(link);
  const queue = [
    new URL("/sitemap.xml", origin).href,
    new URL("/wp-sitemap.xml", origin).href,
  ];
  const seen = new Set<string>();
  const sitemaps: string[] = [];
  let truncated = false;
  while (queue.length && seen.size < 20 && urls.size < 2001) {
    const sitemap = queue.shift()!;
    if (seen.has(sitemap) || new URL(sitemap).origin !== origin) continue;
    seen.add(sitemap);
    try {
      const response = await fetcher(sitemap);
      if (
        response.status !== 200 ||
        !/<(sitemapindex|urlset)\b/i.test(response.body) ||
        new URL(response.url).origin !== origin
      )
        continue;
      sitemaps.push(sitemap);
      emit("sitemap.discovered", { url: sitemap });
      for (const loc of candidates(
        response.body,
        /<loc\b[^>]*>([^<]+)<\/loc>/gi,
      )) {
        if (/<sitemapindex\b/i.test(response.body)) {
          try {
            const url = new URL(loc, sitemap);
            if (url.origin === origin) queue.push(url.href);
          } catch {
            /* malformed */
          }
        } else add(loc);
      }
    } catch {
      /* optional sitemap unavailable; reachability already succeeded */
    }
  }
  truncated = urls.size >= 2001 || queue.length > 0;
  const inventory = {
    urls: [...urls].map((url) => ({ url, kind: classify(url) })),
    count: urls.size,
    truncated,
    sitemaps,
    wordpress,
    woocommerce,
  };
  emit("url_count.completed", { count: inventory.count, truncated });
  return inventory;
}
export function selectPages(inventory: Inventory, scope: Scope) {
  const safe = inventory.urls.filter(
    (item) => !["cart", "checkout", "account", "search"].includes(item.kind),
  );
  const home = safe.find((item) => item.kind === "homepage") ?? safe[0];
  const sorted = [...safe].sort(
    (a, b) => Number(b.kind === "product") - Number(a.kind === "product"),
  );
  const unique = [
    ...new Map(
      [home, ...sorted].filter(Boolean).map((item) => [item.url, item]),
    ).values(),
  ];
  return unique.slice(
    0,
    scope === "free" ? 2 : scope === "major5" ? 5 : scope === "retest" ? 1 : 8,
  );
}
