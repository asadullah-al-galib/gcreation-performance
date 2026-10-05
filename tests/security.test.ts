import test from "node:test";
import assert from "node:assert/strict";
import { safeFetch, SecurityError } from "../packages/shared/src/security.js";
import { createEgressProxy } from "../packages/scanner/src/proxy.js";
import { request } from "node:http";
import { once } from "node:events";

test("safeFetch rejects a redirect to private or unsupported targets before transport", async () => {
  for (const destination of [
    "http://127.0.0.1/",
    "http://169.254.169.254/latest/",
    "http://192.168.1.1/",
    "file:///etc/passwd",
  ]) {
    let hops = 0;
    await assert.rejects(
      safeFetch("https://example.com/", {
        resolver: async () => [{ address: "8.8.8.8", family: 4 }],
        transport: async (target) => {
          hops++;
          return {
            url: target.url.href,
            status: 302,
            headers: { location: destination },
            body: "",
            ttfbMs: 1,
          };
        },
      }),
      SecurityError,
    );
    assert.equal(hops, 1);
  }
});
test("safeFetch follows bounded safe redirects and pins transport destinations", async () => {
  const addresses: string[] = [];
  const result = await safeFetch("https://example.com/", {
    resolver: async () => [{ address: "8.8.8.8", family: 4 }],
    transport: async (target) => {
      addresses.push(target.address);
      return {
        url: target.url.href,
        status: target.url.pathname === "/" ? 301 : 200,
        headers: (target.url.pathname === "/"
          ? { location: "/final" }
          : {}) as Record<string, string>,
        body: "ok",
        ttfbMs: 1,
      };
    },
  });
  assert.equal(result.redirects, 1);
  assert.deepEqual(addresses, ["8.8.8.8", "8.8.8.8"]);
  await assert.rejects(
    safeFetch("https://example.com/", {
      maxRedirects: 1,
      resolver: async () => [{ address: "8.8.8.8", family: 4 }],
      transport: async (target) => ({
        url: target.url.href,
        status: 302,
        headers: { location: "/loop" },
        body: "",
        ttfbMs: 1,
      }),
    }),
    SecurityError,
  );
});
test("egress HTTP and CONNECT reject local destinations through a real proxy socket", async () => {
  const proxy = createEgressProxy();
  proxy.listen(0, "127.0.0.1");
  await once(proxy, "listening");
  const address = proxy.address();
  assert.ok(address && typeof address !== "string");
  const get = () =>
    new Promise<number>((resolve, reject) => {
      const req = request(
        {
          host: "127.0.0.1",
          port: address.port,
          path: "http://127.0.0.1:3101/health",
          method: "GET",
        },
        (res) => {
          res.resume();
          resolve(res.statusCode!);
        },
      );
      req.on("error", reject);
      req.end();
    });
  assert.equal(await get(), 403);
  const connect = () =>
    new Promise<number>((resolve, reject) => {
      const req = request({
        host: "127.0.0.1",
        port: address.port,
        path: "169.254.169.254:443",
        method: "CONNECT",
      });
      req.on("connect", (res, socket) => {
        resolve(res.statusCode!);
        socket.destroy();
      });
      req.on("error", reject);
      req.end();
    });
  assert.equal(await connect(), 403);
  proxy.close();
  await once(proxy, "close");
});
