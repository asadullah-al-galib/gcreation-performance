import { createServer, request } from "node:http";
import { timingSafeEqual } from "node:crypto";
import { pathToFileURL } from "node:url";

// This code is baked into the reviewed image; no release mount is permitted.
export function createGateway(engineSecret, appSecret, upstream) {
  if (
    ![engineSecret, appSecret].every((s) => /^[0-9a-f]{64}$/.test(s)) ||
    engineSecret === appSecret
  )
    throw new Error("Distinct gateway credentials required");
  const target = new URL(upstream);
  if (
    target.protocol !== "http:" ||
    target.username ||
    target.password ||
    target.pathname !== "/" ||
    target.search ||
    target.hash
  )
    throw new Error("Fixed internal upstream required");
  const server = createServer((req, res) => {
    const health = req.url === "/health" && req.method === "GET";
    const supplied = Buffer.from(String(req.headers["x-engine-secret"] ?? ""));
    const expected = Buffer.from(engineSecret);
    if (
      !health &&
      (supplied.length !== expected.length ||
        !timingSafeEqual(supplied, expected))
    ) {
      res.writeHead(401);
      res.end();
      return;
    }
    if (
      !["GET", "POST"].includes(req.method) ||
      !req.url?.startsWith("/") ||
      req.url.startsWith("//") ||
      /[\x00-\x20\\]/.test(req.url) ||
      req.url.length > 4096
    ) {
      res.writeHead(400);
      res.end();
      return;
    }
    let size = 0;
    const chunks = [];
    req.on("data", (chunk) => {
      size += chunk.length;
      if (size > 1024 * 1024) {
        res.writeHead(413);
        res.end();
        req.destroy();
      } else chunks.push(chunk);
    });
    req.on("end", () => {
      if (res.writableEnded) return;
      const body = Buffer.concat(chunks);
      const headers = {
        "content-type": "application/json",
        "content-length": body.length,
      };
      // Do not copy arbitrary client headers, cookies, proxy credentials or the master secret.
      if (!health) headers["x-engine-secret"] = appSecret;
      const client = req.headers["x-client-key"];
      if (
        !health &&
        typeof client === "string" &&
        /^[0-9a-f]{64}$/.test(client)
      )
        headers["x-client-key"] = client;
      const forward = request(
        {
          hostname: target.hostname,
          port: target.port,
          path: req.url,
          method: req.method,
          headers,
          agent: false,
        },
        (response) => {
          // Never follow or relay an upstream redirect to a browser. Only content type is relayed.
          if (
            (response.statusCode ?? 500) >= 300 &&
            (response.statusCode ?? 500) < 400
          ) {
            response.destroy();
            res.writeHead(502);
            res.end();
            return;
          }
          res.writeHead(response.statusCode ?? 502, {
            "content-type":
              response.headers["content-type"] ?? "application/json",
            "cache-control": "no-store",
          });
          let bytes = 0;
          response.on("data", (chunk) => {
            bytes += chunk.length;
            if (bytes > 4 * 1024 * 1024) {
              response.destroy();
              res.destroy();
            } else if (!res.write(chunk)) response.pause();
          });
          res.on("drain", () => response.resume());
          response.on("end", () => res.end());
          response.on("error", () => res.destroy());
        },
      );
      const timer = setTimeout(
        () => forward.destroy(new Error("Gateway deadline")),
        60000,
      );
      forward.on("close", () => clearTimeout(timer));
      forward.on("error", () => {
        if (!res.headersSent) res.writeHead(502);
        res.end();
      });
      res.on("close", () => forward.destroy());
      forward.end(body);
    });
    req.on("error", () => res.destroy());
  });
  server.maxConnections = 64;
  server.requestTimeout = 15000;
  server.headersTimeout = 10000;
  server.maxHeadersCount = 32;
  return server;
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(process.argv[1]).href
) {
  const server = createGateway(
    process.env.ENGINE_SECRET,
    process.env.APP_GATEWAY_SECRET,
    "http://gcreation-perf-dev-app:3101/",
  );
  server.listen(3101, "0.0.0.0");
  for (const signal of ["SIGTERM", "SIGINT"])
    process.on(signal, () => {
      server.close();
      setTimeout(() => process.exit(0), 1000).unref();
    });
}
