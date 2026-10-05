import { createEgressProxy, createFetchBridge } from "./proxy.js";
const secret = process.env.FETCH_PROXY_SECRET;
if (!secret || secret.length < 32)
  throw new Error("FETCH_PROXY_SECRET is required");
const proxy = createEgressProxy();
const bridge = createFetchBridge(secret);
proxy.listen(3102, "0.0.0.0");
bridge.listen(3103, "0.0.0.0");
for (const signal of ["SIGTERM", "SIGINT"])
  process.on(signal, () => {
    proxy.close();
    bridge.close();
    setTimeout(() => process.exit(0), 1000).unref();
  });
