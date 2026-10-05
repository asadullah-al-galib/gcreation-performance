import test from "node:test";
import assert from "node:assert/strict";
import {
  safeFetch,
  SecurityError,
  validateTarget,
} from "../packages/shared/src/security.js";
import {
  createEgressProxy,
  createFetchBridge,
} from "../packages/scanner/src/proxy.js";
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
  const get = (target = "http://127.0.0.1:3101/health") =>
    new Promise<number>((resolve, reject) => {
      const req = request(
        {
          host: "127.0.0.1",
          port: address.port,
          path: target,
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
  assert.equal(await get("http://103.112.63.86/"), 403);
  const connect = (target = "169.254.169.254:443") =>
    new Promise<number>((resolve, reject) => {
      const req = request({
        host: "127.0.0.1",
        port: address.port,
        path: target,
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
  assert.equal(await connect("103.112.63.86:443"), 403);
  proxy.close();
  await once(proxy, "close");
});

test("hard policy denies raw server IP even without configured deny list", async () => {
  await assert.rejects(validateTarget("http://103.112.63.86/"), SecurityError);
  await assert.rejects(
    validateTarget("https://controlled.example/", async () => [
      { address: "103.112.63.86", family: 4 },
    ]),
    SecurityError,
  );
});

test("fetch bridge accepts only its scoped credential and rejects raw self host", async () => {
  const secret = "c".repeat(64);
  const bridge = createFetchBridge(secret);
  bridge.listen(0, "127.0.0.1");
  await once(bridge, "listening");
  const address = bridge.address();
  assert.ok(address && typeof address !== "string");
  try {
    const url = `http://127.0.0.1:${address.port}/fetch`;
    const body = JSON.stringify({ url: "http://103.112.63.86/" });
    const oldAuth = await fetch(url, {
      method: "POST",
      headers: { "x-engine-secret": secret },
      body,
    });
    assert.equal(oldAuth.status, 403);
    const scoped = await fetch(url, {
      method: "POST",
      headers: { "x-fetch-proxy-secret": secret },
      body,
    });
    assert.equal(scoped.status, 422);
  } finally {
    bridge.closeAllConnections();
    bridge.close();
    await once(bridge, "close");
  }
});
