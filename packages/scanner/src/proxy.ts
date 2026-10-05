import { createServer, request as forwardHttp } from "node:http";
import { connect } from "node:net";
import type { Duplex } from "node:stream";
import {
  validateTarget,
  safeFetch,
  type Resolver,
  systemResolver,
} from "../../shared/src/security.js";
import { secretMatches } from "../../shared/src/auth.js";
export function createEgressProxy(resolver: Resolver = systemResolver) {
  const server = createServer(async (req, res) => {
    let outgoing: ReturnType<typeof forwardHttp> | undefined;
    try {
      if (req.method !== "GET" && req.method !== "HEAD")
        throw new Error("Only read-only scan requests are allowed");
      const target = await validateTarget(req.url ?? "", resolver);
      if (target.url.protocol !== "http:")
        throw new Error("HTTPS requires CONNECT");
      const headers = { ...req.headers, host: target.url.host };
      delete headers["proxy-authorization"];
      delete headers.authorization;
      delete headers.cookie;
      outgoing = forwardHttp(
        target.url,
        {
          method: req.method,
          headers,
          agent: false,
          lookup: (_h, _o, cb) => cb(null, target.address, target.family),
        },
        (upstream) => {
          res.writeHead(upstream.statusCode ?? 502, upstream.headers);
          let bytes = 0;
          upstream.on("data", (chunk: Buffer) => {
            bytes += chunk.length;
            if (bytes > 15 * 1024 * 1024)
              upstream.destroy(new Error("Resource limit"));
          });
          upstream.on("error", () => res.destroy());
          upstream.pipe(res);
        },
      );
      outgoing.setTimeout(15000, () => outgoing?.destroy());
      outgoing.on("error", () => {
        if (!res.headersSent) res.writeHead(502);
        res.end();
      });
      outgoing.end();
      res.on("close", () => outgoing?.destroy());
    } catch {
      if (!res.headersSent) res.writeHead(403);
      res.end("Destination rejected");
      outgoing?.destroy();
    }
  });
  server.on("connect", async (req, client, head) => {
    let remote: ReturnType<typeof connect> | undefined;
    try {
      if (!req.url || !/^[a-zA-Z0-9.\-[\]:]+:443$/.test(req.url))
        throw new Error("Only public HTTPS tunnels are allowed");
      const target = await validateTarget(`https://${req.url}/`, resolver);
      remote = connect({ host: target.address, port: 443 });
      const deadline = setTimeout(() => {
        remote?.destroy();
        client.destroy();
      }, 30000);
      remote.on("connect", () => {
        client.write("HTTP/1.1 200 Connection Established\r\n\r\n");
        if (head.length) remote!.write(head);
        remote!.pipe(client);
        client.pipe(remote!);
      });
      let bytes = 0;
      const bound = (chunk: Buffer) => {
        bytes += chunk.length;
        if (bytes > 20 * 1024 * 1024) {
          remote?.destroy();
          client.destroy();
        }
      };
      remote.on("data", bound);
      client.on("data", bound);
      const clean = () => {
        clearTimeout(deadline);
        remote?.destroy();
        client.destroy();
      };
      remote.on("error", clean);
      client.on("error", clean);
      client.on("close", clean);
      remote.on("close", () => {
        clearTimeout(deadline);
        client.destroy();
      });
    } catch {
      client.end("HTTP/1.1 403 Forbidden\r\n\r\n");
      remote?.destroy();
    }
  });
  server.maxConnections = 64;
  server.requestTimeout = 15000;
  server.headersTimeout = 10000;
  return server;
}
export function createFetchBridge(secret: string) {
  return createServer(async (req, res) => {
    try {
      if (
        req.method !== "POST" ||
        req.url !== "/fetch" ||
        !secretMatches(String(req.headers["x-engine-secret"] ?? ""), secret)
      ) {
        res.writeHead(403);
        res.end();
        return;
      }
      let body = "";
      for await (const chunk of req) {
        body += String(chunk);
        if (body.length > 4096) throw new Error("Body limit");
      }
      const data = JSON.parse(body) as { url: string; method?: "GET" | "HEAD" };
      const result = await safeFetch(data.url, {
        method: data.method === "HEAD" ? "HEAD" : "GET",
      });
      // Only useful diagnostic headers are returned; never relay cookies.
      for (const key of Object.keys(result.headers))
        if (
          ![
            "content-type",
            "cache-control",
            "content-encoding",
            "link",
          ].includes(key)
        )
          delete result.headers[key];
      res.setHeader("content-type", "application/json");
      res.end(JSON.stringify(result));
    } catch {
      res.writeHead(422);
      res.end(JSON.stringify({ error: "URL fetch failed or was rejected" }));
    }
  });
}
export function closeProxySockets(socket: Duplex) {
  socket.destroy();
}
