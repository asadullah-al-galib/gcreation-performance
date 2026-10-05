import test from "node:test";
import assert from "node:assert/strict";
import { chromium, type Browser } from "playwright";
import { scanPage } from "../packages/scanner/src/index.js";

test("scanner closes the browser after a navigation failure while keeping sandbox/proxy controls", async (t) => {
  let closes = 0;
  let launchOptions: Parameters<typeof chromium.launch>[0];
  const page = {
    on: () => {},
    goto: async () => {
      throw new Error("controlled navigation failure");
    },
  };
  const context = {
    newPage: async () => page,
    route: async () => {},
    routeWebSocket: async () => {},
  };
  const browser = {
    newContext: async () => context,
    close: async () => {
      closes++;
    },
  };
  t.mock.method(
    chromium,
    "launch",
    async (options: Parameters<typeof chromium.launch>[0]) => {
      launchOptions = options;
      return browser as unknown as Browser;
    },
  );
  const previous = process.env.BROWSER_PROXY;
  process.env.BROWSER_PROXY = "http://127.0.0.1:3102";
  try {
    await assert.rejects(
      scanPage("https://8.8.8.8/", false, () => {}),
      /controlled navigation failure/,
    );
    assert.equal(closes, 1);
    assert.equal(launchOptions?.chromiumSandbox, true);
    assert.equal(launchOptions?.proxy?.bypass, "<-loopback>");
    assert.ok(!launchOptions?.args?.includes("--no-sandbox"));
  } finally {
    if (previous === undefined) delete process.env.BROWSER_PROXY;
    else process.env.BROWSER_PROXY = previous;
  }
});
test("scanner refuses browser work without a validating egress proxy", async () => {
  const previous = process.env.BROWSER_PROXY;
  delete process.env.BROWSER_PROXY;
  try {
    await assert.rejects(
      scanPage("https://8.8.8.8/", false, () => {}),
      /egress proxy is required/,
    );
  } finally {
    if (previous !== undefined) process.env.BROWSER_PROXY = previous;
  }
});
