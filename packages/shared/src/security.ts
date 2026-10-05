import { lookup } from "node:dns/promises";
import { request as httpRequest } from "node:http";
import { request as httpsRequest } from "node:https";
import ipaddr from "ipaddr.js";

export class SecurityError extends Error {}
export type Resolver = (
  hostname: string,
) => Promise<{ address: string; family: number }[]>;
export const systemResolver: Resolver = (host) =>
  lookup(host, { all: true, verbatim: true });
const forbiddenHosts = new Set([
  "localhost",
  "metadata.google.internal",
  "dev.gcreation.agency",
  "performance.gcreation.agency",
]);
export function parsePublicUrl(input: string): URL {
  if (input.length > 2048 || /[\x00-\x20\\]/.test(input))
    throw new SecurityError("Invalid URL");
  let url: URL;
  try {
    url = new URL(input);
  } catch {
    throw new SecurityError("Invalid URL");
  }
  if (!["http:", "https:"].includes(url.protocol))
    throw new SecurityError("Only HTTP and HTTPS are supported");
  if (
    [...url.searchParams.keys()].some((key) =>
      /token|password|secret|session|auth|api[_-]?key/i.test(key),
    )
  )
    throw new SecurityError("Credential-like URL parameters are not supported");
  if (url.username || url.password || url.hash || url.port)
    throw new SecurityError(
      "Credentials, fragments and non-default ports are not supported",
    );
  const host = url.hostname
    .replace(/^\[|\]$/g, "")
    .replace(/\.$/, "")
    .toLowerCase();
  if (
    forbiddenHosts.has(host) ||
    (!host.includes(".") && !ipaddr.isValid(host)) ||
    /\.(localhost|local|internal|home|lan|test|invalid)$/.test(host)
  )
    throw new SecurityError("Internal or out-of-scope host");
  url.hostname = host.includes(":") ? `[${host}]` : host;
  return url;
}
export function isPublicIp(address: string): boolean {
  if (
    !ipaddr.isValid(address) ||
    ["168.63.129.16", "103.112.63.86"].includes(address)
  )
    return false;
  const parsed = ipaddr.parse(address);
  if (parsed.kind() === "ipv6" && (parsed as ipaddr.IPv6).isIPv4MappedAddress())
    return false;
  if (parsed.range() !== "unicast") return false;
  // Avoid protocol-assignment/reserved IPv4 and translation/tunnelling IPv6 ranges.
  const extra = [
    "192.0.0.0/24",
    "192.0.2.0/24",
    "198.51.100.0/24",
    "203.0.113.0/24",
    "100.64.0.0/10",
    "198.18.0.0/15",
    "64:ff9b::/96",
    "2001::/32",
    "2002::/16",
  ];
  return !extra.some((cidr) => {
    const [net, bits] = ipaddr.parseCIDR(cidr);
    return net.kind() === parsed.kind() && parsed.match(net, bits);
  });
}
export async function validateTarget(
  input: string,
  resolve: Resolver = systemResolver,
) {
  const url = parsePublicUrl(input);
  const host = url.hostname.replace(/^\[|\]$/g, "");
  const resolveWithDeadline: Resolver = async (hostname) => {
    let timer: ReturnType<typeof setTimeout> | undefined;
    try {
      return await Promise.race([
        resolve(hostname),
        new Promise<never>((_done, reject) => {
          timer = setTimeout(
            () => reject(new SecurityError("DNS deadline exceeded")),
            5000,
          );
        }),
      ]);
    } finally {
      if (timer) clearTimeout(timer);
    }
  };
  const addresses = ipaddr.isValid(host)
    ? [{ address: host, family: ipaddr.parse(host).kind() === "ipv4" ? 4 : 6 }]
    : await resolveWithDeadline(host);
  const denied = (process.env.DENIED_IPS ?? "")
    .split(",")
    .filter((address) => ipaddr.isValid(address))
    .map((address) => ipaddr.parse(address).toNormalizedString());
  if (
    !addresses.length ||
    addresses.some(
      (item) =>
        !isPublicIp(item.address) ||
        denied.includes(ipaddr.parse(item.address).toNormalizedString()),
    )
  )
    throw new SecurityError("Destination resolves to a blocked IP");
  return { url, address: addresses[0].address, family: addresses[0].family };
}
export interface SafeResponse {
  url: string;
  status: number;
  headers: Record<string, string>;
  body: string;
  redirects: number;
  ttfbMs: number;
}
export async function safeFetch(
  input: string,
  options: {
    resolver?: Resolver;
    maxBytes?: number;
    timeoutMs?: number;
    maxRedirects?: number;
    method?: "GET" | "HEAD";
    transport?: (
      target: Awaited<ReturnType<typeof validateTarget>>,
    ) => Promise<Omit<SafeResponse, "redirects">>;
  } = {},
): Promise<SafeResponse> {
  if (process.env.FETCH_BRIDGE_URL) {
    await validateTarget(input, options.resolver);
    const response = await fetch(process.env.FETCH_BRIDGE_URL + "/fetch", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-fetch-proxy-secret": process.env.FETCH_PROXY_SECRET ?? "",
      },
      body: JSON.stringify({ url: input, method: options.method ?? "GET" }),
      signal: AbortSignal.timeout(60000),
      redirect: "error",
    });
    if (!response.ok)
      throw new SecurityError("Validated egress fetch rejected");
    return (await response.json()) as SafeResponse;
  }
  let target = input;
  const maxRedirects = options.maxRedirects ?? 5;
  for (let redirects = 0; redirects <= maxRedirects; redirects++) {
    const validated = await validateTarget(target, options.resolver);
    const response = options.transport
      ? await options.transport(validated)
      : await new Promise<Omit<SafeResponse, "redirects">>(
          (resolve, reject) => {
            const start = performance.now();
            const request = (
              validated.url.protocol === "https:" ? httpsRequest : httpRequest
            )(
              validated.url,
              {
                method: options.method ?? "GET",
                agent: false,
                lookup: (_host, _options, cb) =>
                  cb(null, validated.address, validated.family),
                headers: {
                  "User-Agent": "gCreation-PerformanceDoctor/0.1",
                  "Accept-Encoding": "identity",
                },
              },
              (res) => {
                const ttfbMs = performance.now() - start;
                let bytes = 0;
                const chunks: Buffer[] = [];
                const headers: Record<string, string> = {};
                for (const [key, value] of Object.entries(res.headers))
                  if (value !== undefined)
                    headers[key] = Array.isArray(value)
                      ? value.join(", ")
                      : value;
                res.on("data", (chunk: Buffer) => {
                  bytes += chunk.length;
                  if (bytes > (options.maxBytes ?? 2 * 1024 * 1024))
                    res.destroy(new Error("Response size limit exceeded"));
                  else chunks.push(chunk);
                });
                res.on("error", reject);
                res.on("end", () =>
                  resolve({
                    url: validated.url.href,
                    status: res.statusCode ?? 0,
                    headers,
                    body: Buffer.concat(chunks).toString("utf8"),
                    ttfbMs,
                  }),
                );
              },
            );
            const timer = setTimeout(
              () => request.destroy(new Error("Request deadline exceeded")),
              options.timeoutMs ?? 10000,
            );
            request.on("close", () => clearTimeout(timer));
            request.on("error", reject);
            request.end();
          },
        );
    if (
      [301, 302, 303, 307, 308].includes(response.status) &&
      response.headers.location
    ) {
      if (redirects === maxRedirects)
        throw new SecurityError("Redirect limit exceeded");
      target = new URL(response.headers.location, response.url).href;
      await validateTarget(target, options.resolver);
      continue;
    }
    return { ...response, redirects };
  }
  throw new SecurityError("Redirect limit exceeded");
}
