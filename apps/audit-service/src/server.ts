import Fastify from "fastify";
import type { Store } from "./store.js";
import { randomUUID } from "node:crypto";
import { validateTarget } from "../../../packages/shared/src/security.js";
import {
  hashToken,
  secretMatches,
  reportAuthorized,
} from "../../../packages/shared/src/auth.js";
import { quote } from "../../../packages/shared/src/pricing.js";
import { compare } from "../../../packages/report-engine/src/index.js";
import type { Mode } from "../../../packages/contracts/src/index.js";
export function createApp(store: Store, secret: string) {
  if (secret.length < 32) throw new Error("A strong engine secret is required");
  const app = Fastify({
    logger: { level: "info", redact: ["req.headers", "req.body", "req.url"] },
    logController: new Fastify.LogController({ disableRequestLogging: true }),
    bodyLimit: 8192,
    requestTimeout: 15000,
    trustProxy: false,
  });
  const attempts = new Map<string, { count: number; reset: number }>();
  app.addHook("onRequest", async (req, reply) => {
    if (req.url === "/health") return;
    const item = attempts.get(req.ip) ?? {
      count: 0,
      reset: Date.now() + 60000,
    };
    if (item.reset < Date.now()) {
      item.count = 0;
      item.reset = Date.now() + 60000;
    }
    item.count++;
    attempts.set(req.ip, item);
    if (attempts.size > 1000)
      for (const [key, value] of attempts)
        if (value.reset < Date.now()) attempts.delete(key);
    if (item.count > 120)
      return reply.code(429).send({ error: "Rate limit reached" });
    if (!secretMatches(String(req.headers["x-engine-secret"] ?? ""), secret))
      return reply.code(401).send({ error: "Unauthorized" });
  });
  app.setErrorHandler((error, _req, reply) => {
    app.log.warn({
      event: "request.rejected",
      errorType: error instanceof Error ? error.name : "UnknownError",
    });
    reply.code(422).send({ error: "Request invalid or operation unavailable" });
  });
  app.get("/health", async () => ({
    ok: true,
    service: "gcreation-performance",
    environment: "development",
    version: "0.1.0",
    browserConcurrency: 1,
  }));
  app.post<{ Body: { url: string } }>("/audits", async (req, reply) => {
    if (typeof req.body?.url !== "string")
      return reply.code(400).send({ error: "URL required" });
    const count = store.db
      .prepare(
        "SELECT count(*) AS n FROM jobs WHERE state IN ('PENDING','RUNNING','WAITING_FOR_RESOURCES','RETRYING')",
      )
      .get();
    if (Number(count?.n) >= 50)
      return reply.code(429).send({ error: "Queue full; please try later" });
    const target = await validateTarget(req.body.url);
    const id = store.transaction(() => store.createAudit(target.url.href));
    return reply.code(202).send({ id, state: "PENDING" });
  });
  app.get<{ Params: { id: string } }>("/audits/:id", async (req, reply) => {
    const audit = store.getAudit(req.params.id);
    if (!audit) return reply.code(404).send({ error: "Not found" });
    if (audit.scope !== "free")
      return reply
        .code(403)
        .send({ error: "Paid report authorization required" });
    return audit;
  });
  app.get<{ Params: { id: string }; Querystring: { after?: string } }>(
    "/audits/:id/events",
    async (req, reply) => {
      if (!store.getAudit(req.params.id))
        return reply.code(404).send({ error: "Not found" });
      const after = Number(req.query.after ?? 0);
      if (!Number.isSafeInteger(after) || after < 0)
        return reply.code(400).send({ error: "Invalid event offset" });
      return store.db
        .prepare(
          "SELECT id,type,data,created_at FROM audit_events WHERE audit_id=? AND id>? ORDER BY id LIMIT 200",
        )
        .all(req.params.id, after)
        .map((row) => ({ ...row, data: JSON.parse(String(row.data)) }));
    },
  );
  app.get<{ Params: { id: string } }>(
    "/audits/:id/stream",
    async (req, reply) => {
      if (!store.getAudit(req.params.id))
        return reply.code(404).send({ error: "Not found" });
      const offset = Number(req.headers["last-event-id"] ?? 0);
      if (!Number.isSafeInteger(offset) || offset < 0)
        return reply.code(400).send({ error: "Invalid event offset" });
      reply.hijack();
      reply.raw.writeHead(200, {
        "content-type": "text/event-stream",
        "cache-control": "no-store",
        "x-accel-buffering": "no",
        connection: "keep-alive",
      });
      let after = offset;
      const send = () => {
        for (const event of store.db
          .prepare(
            "SELECT id,type,data FROM audit_events WHERE audit_id=? AND id>? ORDER BY id LIMIT 200",
          )
          .all(req.params.id, after)) {
          reply.raw.write(
            `id: ${event.id}\nevent: ${event.type}\ndata: ${event.data}\n\n`,
          );
          after = Number(event.id);
        }
        if (
          ["COMPLETED", "FAILED"].includes(store.getAudit(req.params.id)!.state)
        )
          reply.raw.end();
      };
      send();
      if (reply.raw.writableEnded) return;
      const interval = setInterval(send, 500);
      const heartbeat = setInterval(
        () => reply.raw.write(": heartbeat\n\n"),
        15000,
      );
      const deadline = setTimeout(() => reply.raw.end(), 180000);
      reply.raw.on("close", () => {
        clearInterval(interval);
        clearInterval(heartbeat);
        clearTimeout(deadline);
      });
    },
  );
  app.post<{ Body: { auditId: string; scope: "major5" | "full"; mode: Mode } }>(
    "/quotes",
    async (req, reply) => {
      const audit = store.getAudit(req.body.auditId);
      if (
        !audit?.inventory ||
        audit.state !== "COMPLETED" ||
        audit.scope !== "free"
      )
        return reply.code(409).send({ error: "Completed free scan required" });
      const result = quote(
        req.body.scope,
        audit.inventory.count,
        req.body.mode,
      );
      store.analytics(audit.id, "paid.package_selected", {
        scope: result.scope,
        mode: result.mode,
        tier: result.tier,
      });
      return { ...result, websiteUrl: audit.url };
    },
  );
  app.post<{
    Body: {
      wcOrderId: string;
      auditId: string;
      scope: "major5" | "full";
      mode: Mode;
      contact: string;
      reportToken: string;
      amount: number;
      currency: string;
    };
  }>("/orders/paid", async (req, reply) => {
    const data = req.body;
    if (
      !/^\d{1,20}$/.test(data.wcOrderId) ||
      !data.contact.includes("@") ||
      data.contact.length > 254 ||
      !/^[A-Za-z0-9_-]{40,128}$/.test(data.reportToken)
    )
      return reply.code(400).send({ error: "Invalid paid order" });
    const prior = store.db
      .prepare("SELECT * FROM orders WHERE wc_order_id=?")
      .get(data.wcOrderId);
    if (prior) return { auditId: prior.audit_id, idempotent: true };
    const free = store.getAudit(data.auditId);
    if (!free?.inventory || free.state !== "COMPLETED" || free.scope !== "free")
      return reply.code(409).send({ error: "Completed free audit required" });
    const pricing = quote(data.scope, free.inventory.count, data.mode);
    if (
      pricing.amount === null ||
      data.amount !== pricing.amount ||
      data.currency !== pricing.currency
    )
      return reply
        .code(409)
        .send({ error: "Payment does not match trusted quote" });
    const id = store.transaction(() => {
      const contactHash = hashToken(data.contact.trim().toLowerCase());
      const existing = store.db
        .prepare("SELECT id FROM customers WHERE contact_hash=?")
        .get(contactHash);
      const customer = String(existing?.id ?? randomUUID());
      if (!existing)
        store.db
          .prepare("INSERT INTO customers VALUES(?,?)")
          .run(customer, contactHash);
      const auditId = store.createAudit(free.url, data.scope, free.id);
      store.saveInventory(auditId, free.inventory!);
      const orderId = randomUUID();
      store.db
        .prepare("INSERT INTO orders VALUES(?,?,?,?,?,?,?,?,?,?,?,?)")
        .run(
          orderId,
          data.wcOrderId,
          auditId,
          free.id,
          customer,
          pricing.amount,
          pricing.currency,
          data.scope,
          data.mode,
          pricing.tier,
          hashToken(data.reportToken),
          new Date().toISOString(),
        );
      if (data.mode === "expert")
        store.db
          .prepare("INSERT INTO expert_tasks VALUES(?,?,?,?,?)")
          .run(
            randomUUID(),
            auditId,
            orderId,
            "Pending",
            new Date().toISOString(),
          );
      store.analytics(auditId, "paid.conversion", {
        scope: data.scope,
        mode: data.mode,
        tier: pricing.tier,
      });
      return auditId;
    });
    return reply.code(201).send({ auditId: id, idempotent: false });
  });
  app.post<{
    Body: {
      token: string;
      orderId: string;
      contact: string;
      action?: string;
      ruleId?: string;
      url?: string;
    };
  }>("/reports/access", async (req, reply) => {
    const data = req.body;
    const order = store.db
      .prepare(
        "SELECT o.*,c.contact_hash FROM orders o JOIN customers c ON c.id=o.customer_id WHERE o.wc_order_id=?",
      )
      .get(data.orderId);
    if (
      !order ||
      !reportAuthorized(
        data.token,
        String(order.report_token_hash),
        data.orderId,
        String(order.wc_order_id),
        data.contact,
        String(order.contact_hash),
      )
    )
      return reply.code(403).send({ error: "Verification failed" });
    const audit = store.getAudit(String(order.audit_id))!;
    if (data.action === "fixed") {
      const change = store.db
        .prepare(
          "UPDATE issues SET claimed_fixed=1 WHERE audit_id=? AND rule_id=? AND url=?",
        )
        .run(audit.id, data.ruleId ?? "", data.url ?? "");
      if (!change.changes)
        return reply.code(404).send({ error: "Issue not found" });
      return { claimedFixed: true, verified: false };
    }
    if (data.action === "expert") {
      store.db
        .prepare("INSERT OR IGNORE INTO expert_tasks VALUES(?,?,?,?,?)")
        .run(
          randomUUID(),
          audit.id,
          order.id,
          "Pending",
          new Date().toISOString(),
        );
      store.analytics(audit.id, "expert.request", {});
      return { state: "Pending" };
    }
    if (data.action === "retest") {
      if (
        !audit.report ||
        !audit.report.pages.some((page) => page.url === data.url)
      )
        return reply.code(400).send({ error: "Choose an audited page" });
      const id = store.transaction(() =>
        store.createAudit(data.url!, "retest", audit.id),
      );
      store.analytics(audit.id, "retest.used", {});
      return { auditId: id };
    }
    const retests = store.db
      .prepare(
        "SELECT id FROM audits WHERE parent_id=? AND scope='retest' ORDER BY created_at DESC LIMIT 5",
      )
      .all(audit.id)
      .map((row) => store.getAudit(String(row.id))!);
    return {
      audit,
      claimedFixed: store.db
        .prepare(
          "SELECT rule_id,url,claimed_fixed FROM issues WHERE audit_id=?",
        )
        .all(audit.id),
      retests: retests.map((item) => ({
        id: item.id,
        state: item.state,
        comparison:
          audit.report && item.report
            ? compare(audit.report, item.report)
            : null,
      })),
    };
  });
  app.post<{ Body: { auditId: string; type: string } }>(
    "/analytics",
    async (req, reply) => {
      if (
        req.body.type !== "free.report_viewed" ||
        store.getAudit(req.body.auditId)?.scope !== "free"
      )
        return reply.code(400).send({ error: "Invalid event" });
      store.analytics(req.body.auditId, req.body.type, {});
      return { ok: true };
    },
  );
  app.post<{ Body: { auditId: string; contact: string } }>(
    "/expert/review",
    async (req, reply) => {
      const audit = store.getAudit(req.body.auditId);
      if (
        !audit?.report ||
        audit.scope !== "free" ||
        typeof req.body.contact !== "string" ||
        !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(req.body.contact)
      )
        return reply
          .code(400)
          .send({ error: "Completed scan and contact required" });
      const id = randomUUID();
      store.db
        .prepare("INSERT OR IGNORE INTO expert_requests VALUES(?,?,?,?,?)")
        .run(
          id,
          audit.id,
          hashToken(req.body.contact.trim().toLowerCase()),
          "Pending",
          new Date().toISOString(),
        );
      const request = store.db
        .prepare("SELECT id,state FROM expert_requests WHERE audit_id=?")
        .get(audit.id)!;
      store.analytics(audit.id, "expert.review_requested", {});
      return request;
    },
  );
  app.patch<{ Params: { id: string }; Body: { state: string; kind: string } }>(
    "/admin/experts/:id",
    async (req, reply) => {
      const states = [
        "Pending",
        "In Review",
        "In Progress",
        "Waiting",
        "Completed",
        "Retest Required",
        "Verified",
      ];
      if (
        !states.includes(req.body.state) ||
        !["task", "review"].includes(req.body.kind)
      )
        return reply.code(400).send({ error: "Invalid expert state" });
      // Verified is evidence-backed: an admin cannot assert it without a successful retest.
      const table =
        req.body.kind === "task" ? "expert_tasks" : "expert_requests";
      const item = store.db
        .prepare(`SELECT audit_id FROM ${table} WHERE id=?`)
        .get(req.params.id);
      if (!item) return reply.code(404).send({ error: "Not found" });
      if (
        req.body.state === "Verified" &&
        !store.db
          .prepare(
            "SELECT id FROM audits WHERE parent_id=? AND scope='retest' AND state='COMPLETED'",
          )
          .get(item.audit_id)
      )
        return reply.code(409).send({
          error:
            "Completed retest required; review measured evidence before marking verified",
        });
      store.db
        .prepare(`UPDATE ${table} SET state=? WHERE id=?`)
        .run(req.body.state, req.params.id);
      return { state: req.body.state };
    },
  );
  app.get("/admin/summary", async () => ({
    audits: store.db
      .prepare(
        "SELECT id,scope,state,created_at FROM audits ORDER BY created_at DESC LIMIT 100",
      )
      .all(),
    orders: store.db
      .prepare(
        "SELECT wc_order_id,audit_id,scope,mode,amount,tier FROM orders ORDER BY created_at DESC LIMIT 100",
      )
      .all(),
    experts: store.db
      .prepare(
        "SELECT id,audit_id,state FROM expert_tasks ORDER BY created_at DESC LIMIT 100",
      )
      .all(),
    expertReviews: store.db
      .prepare(
        "SELECT id,audit_id,state FROM expert_requests ORDER BY created_at DESC LIMIT 100",
      )
      .all(),
    analytics: store.db
      .prepare("SELECT type,count(*) AS count FROM analytics GROUP BY type")
      .all(),
  }));
  return app;
}
