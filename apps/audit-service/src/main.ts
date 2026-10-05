import { mkdir } from "node:fs/promises";
import { dirname } from "node:path";
import { Store } from "./store.js";
import { createApp } from "./server.js";
import { Worker } from "./worker.js";
const secret = process.env.ENGINE_SECRET ?? "";
const path = process.env.DATABASE_PATH ?? ".ops/runtime/audits.sqlite";
await mkdir(dirname(path), { recursive: true });
const store = new Store(path);
store.recover();
const app = createApp(store, secret);
const worker = new Worker(store);
const interval = setInterval(() => void worker.tick(), 1000);
const host = process.env.BIND_HOST ?? "127.0.0.1";
if (!["127.0.0.1", "0.0.0.0"].includes(host))
  throw new Error("Invalid bind host");
if (host === "0.0.0.0" && !process.env.FETCH_BRIDGE_URL)
  throw new Error("Container-only binding requires egress bridge");
await app.listen({ port: 3101, host });
for (const signal of ["SIGTERM", "SIGINT"])
  process.on(signal, async () => {
    worker.stopped = true;
    clearInterval(interval);
    await app.close();
    if (worker.busy) setTimeout(() => process.exit(1), 10000).unref();
    else {
      store.close();
      process.exit(0);
    }
  });
