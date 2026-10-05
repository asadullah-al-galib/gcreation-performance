import assert from "node:assert/strict";
import { createServer } from "node:http";
import { once } from "node:events";
import test from "node:test";
import { createGateway } from "../ops/dev/trusted/gateway.mjs";
const engine = "a".repeat(64),
  hop = "b".repeat(64);
async function fixture(handler) {
  const upstream = createServer(handler);
  upstream.listen(0, "127.0.0.1");
  await once(upstream, "listening");
  const gateway = createGateway(
    engine,
    hop,
    `http://127.0.0.1:${upstream.address().port}/`,
  );
  gateway.listen(0, "127.0.0.1");
  await once(gateway, "listening");
  return {
    url: `http://127.0.0.1:${gateway.address().port}`,
    close: async () => {
      gateway.closeAllConnections();
      upstream.closeAllConnections();
      await Promise.all([
        new Promise((r) => gateway.close(r)),
        new Promise((r) => upstream.close(r)),
      ]);
    },
  };
}
test("trusted ingress authenticates master and forwards only scoped app credential", async () => {
  let observed;
  const f = await fixture((req, res) => {
    observed = req.headers;
    res.setHeader("content-type", "application/json");
    res.end("{}");
  });
  try {
    const response = await fetch(f.url + "/audits", {
      method: "POST",
      headers: {
        "x-engine-secret": engine,
        "x-fetch-proxy-secret": "c".repeat(64),
        "x-client-key": "d".repeat(64),
        cookie: "session=private",
        authorization: "private",
      },
      body: "{}",
    });
    assert.equal(response.status, 200);
    assert.equal(observed["x-engine-secret"], hop);
    assert.equal(observed["x-client-key"], "d".repeat(64));
    assert.equal(observed.cookie, undefined);
    assert.equal(observed.authorization, undefined);
    assert.equal(observed["x-fetch-proxy-secret"], undefined);
    assert.ok(!JSON.stringify(observed).includes(engine));
  } finally {
    await f.close();
  }
});
test("missing, incorrect and app-hop credentials cannot enter master business boundary", async () => {
  let count = 0;
  const f = await fixture((_req, res) => {
    count++;
    res.end("{}");
  });
  try {
    for (const secret of ["", hop, "c".repeat(64)]) {
      const response = await fetch(f.url + "/admin/requests", {
        headers: { "x-engine-secret": secret },
      });
      assert.equal(response.status, 401);
    }
    assert.equal(count, 0);
  } finally {
    await f.close();
  }
});
test("unauthenticated health carries no credential to mutable app", async () => {
  let observed;
  const f = await fixture((req, res) => {
    observed = req.headers;
    res.end("{}");
  });
  try {
    assert.equal(
      (
        await fetch(f.url + "/health", {
          headers: { "x-engine-secret": engine, cookie: "bad" },
        })
      ).status,
      200,
    );
    assert.equal(observed["x-engine-secret"], undefined);
    assert.ok(!JSON.stringify(observed).includes(engine));
  } finally {
    await f.close();
  }
});
test("gateway rejects upstream redirects and never relays sensitive headers", async () => {
  const f = await fixture((req, res) => {
    if (req.url === "/redirect") {
      res.writeHead(302, {
        location: "http://127.0.0.1:1/",
        "x-engine-secret": hop,
      });
      res.end();
    } else {
      res.setHeader("x-engine-secret", hop);
      res.setHeader("set-cookie", "private");
      res.end("{}");
    }
  });
  try {
    const headers = { "x-engine-secret": engine };
    assert.equal(
      (await fetch(f.url + "/redirect", { headers, redirect: "error" })).status,
      502,
    );
    const response = await fetch(f.url + "/audits", { headers });
    assert.equal(response.headers.get("x-engine-secret"), null);
    assert.equal(response.headers.get("set-cookie"), null);
    assert.equal(
      (await fetch(f.url + "//external.example/path", { headers })).status,
      400,
    );
  } finally {
    await f.close();
  }
});
