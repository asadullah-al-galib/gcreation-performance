import { DatabaseSync } from "node:sqlite";
import { randomUUID } from "node:crypto";
import type {
  Audit,
  Inventory,
  Report,
  Scope,
} from "../../../packages/contracts/src/index.js";
export class Store {
  db: DatabaseSync;
  constructor(path: string) {
    this.db = new DatabaseSync(path);
    this.db.exec(
      "PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;",
    );
    this.db.exec(
      `CREATE TABLE IF NOT EXISTS migrations(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL);`,
    );
    const version = this.db
      .prepare("SELECT max(version) AS version FROM migrations")
      .get()?.version;
    if (!version)
      this.db.exec(`BEGIN;
      CREATE TABLE sites(id TEXT PRIMARY KEY, url TEXT UNIQUE NOT NULL, created_at TEXT NOT NULL);
      CREATE TABLE audits(id TEXT PRIMARY KEY, site_id TEXT NOT NULL REFERENCES sites(id), scope TEXT NOT NULL, state TEXT NOT NULL, parent_id TEXT REFERENCES audits(id), inventory TEXT, report TEXT, error TEXT, created_at TEXT NOT NULL);
      CREATE TABLE jobs(id TEXT PRIMARY KEY, audit_id TEXT NOT NULL UNIQUE REFERENCES audits(id), state TEXT NOT NULL, priority INTEGER NOT NULL, attempts INTEGER NOT NULL DEFAULT 0, resource_waits INTEGER NOT NULL DEFAULT 0, available_at INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL, started_at TEXT, finished_at TEXT);
      CREATE UNIQUE INDEX single_running_job ON jobs(state) WHERE state='RUNNING';
      CREATE TABLE audit_pages(id INTEGER PRIMARY KEY, audit_id TEXT NOT NULL REFERENCES audits(id), url TEXT NOT NULL, kind TEXT NOT NULL);
      CREATE TABLE metrics(id INTEGER PRIMARY KEY, page_id INTEGER NOT NULL REFERENCES audit_pages(id), data TEXT NOT NULL);
      CREATE TABLE issues(id INTEGER PRIMARY KEY, audit_id TEXT NOT NULL REFERENCES audits(id), rule_id TEXT NOT NULL, url TEXT NOT NULL, data TEXT NOT NULL, claimed_fixed INTEGER NOT NULL DEFAULT 0);
      CREATE TABLE recommendations(id INTEGER PRIMARY KEY, issue_id INTEGER NOT NULL REFERENCES issues(id), action TEXT NOT NULL);
      CREATE TABLE reports(audit_id TEXT PRIMARY KEY REFERENCES audits(id), data TEXT NOT NULL);
      CREATE TABLE audit_events(id INTEGER PRIMARY KEY, audit_id TEXT NOT NULL REFERENCES audits(id), type TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL);
      CREATE INDEX events_lookup ON audit_events(audit_id,id);
      CREATE TABLE customers(id TEXT PRIMARY KEY, contact_hash TEXT UNIQUE NOT NULL);
      CREATE TABLE orders(id TEXT PRIMARY KEY, wc_order_id TEXT UNIQUE NOT NULL, audit_id TEXT UNIQUE NOT NULL REFERENCES audits(id), free_audit_id TEXT NOT NULL REFERENCES audits(id), customer_id TEXT NOT NULL REFERENCES customers(id), amount INTEGER NOT NULL, currency TEXT NOT NULL, scope TEXT NOT NULL, mode TEXT NOT NULL, tier TEXT NOT NULL, report_token_hash TEXT NOT NULL, created_at TEXT NOT NULL);
      CREATE TABLE expert_tasks(id TEXT PRIMARY KEY, audit_id TEXT NOT NULL REFERENCES audits(id), order_id TEXT NOT NULL REFERENCES orders(id), state TEXT NOT NULL, created_at TEXT NOT NULL, UNIQUE(audit_id,order_id));
      CREATE TABLE analytics(id INTEGER PRIMARY KEY, audit_id TEXT, type TEXT NOT NULL, data TEXT NOT NULL, created_at TEXT NOT NULL);
      INSERT INTO migrations VALUES(1,datetime('now')); COMMIT;`);
    const latest = Number(
      this.db.prepare("SELECT max(version) AS version FROM migrations").get()
        ?.version ?? 0,
    );
    if (latest < 2)
      this.db.exec(`BEGIN;
      CREATE TABLE expert_requests(id TEXT PRIMARY KEY, audit_id TEXT NOT NULL UNIQUE REFERENCES audits(id), contact_hash TEXT NOT NULL, state TEXT NOT NULL, created_at TEXT NOT NULL);
      INSERT INTO migrations VALUES(2,datetime('now')); COMMIT;`);
  }
  transaction<T>(operation: () => T): T {
    this.db.exec("BEGIN IMMEDIATE");
    try {
      const result = operation();
      this.db.exec("COMMIT");
      return result;
    } catch (error) {
      this.db.exec("ROLLBACK");
      throw error;
    }
  }
  createAudit(
    url: string,
    scope: Scope = "free",
    parent: string | null = null,
  ) {
    const id = randomUUID();
    const now = new Date().toISOString();
    const site = this.db.prepare("SELECT id FROM sites WHERE url=?").get(url);
    const siteId = site?.id ?? randomUUID();
    if (!site)
      this.db.prepare("INSERT INTO sites VALUES(?,?,?)").run(siteId, url, now);
    this.db
      .prepare(
        "INSERT INTO audits(id,site_id,scope,state,parent_id,created_at) VALUES(?,?,?,?,?,?)",
      )
      .run(id, siteId, scope, "PENDING", parent, now);
    this.db
      .prepare(
        "INSERT INTO jobs(id,audit_id,state,priority,created_at) VALUES(?,?,?,?,?)",
      )
      .run(randomUUID(), id, "PENDING", scope === "free" ? 0 : 10, now);
    this.emit(id, "scan.started", {});
    this.emit(id, "job.queued", {});
    this.analytics(id, "scan.submitted", { scope });
    return id;
  }
  getAudit(id: string): Audit | null {
    const row = this.db
      .prepare(
        "SELECT a.*,s.url FROM audits a JOIN sites s ON s.id=a.site_id WHERE a.id=?",
      )
      .get(id);
    if (!row) return null;
    return {
      id: String(row.id),
      url: String(row.url),
      scope: row.scope as Scope,
      state: row.state as Audit["state"],
      parent_id: row.parent_id as string | null,
      inventory: row.inventory
        ? (JSON.parse(String(row.inventory)) as Inventory)
        : null,
      report: row.report ? (JSON.parse(String(row.report)) as Report) : null,
      error: row.error as string | null,
    };
  }
  emit(id: string, type: string, data: Record<string, unknown>) {
    this.db
      .prepare(
        "INSERT INTO audit_events(audit_id,type,data,created_at) VALUES(?,?,?,?)",
      )
      .run(id, type, JSON.stringify(data), new Date().toISOString());
  }
  analytics(id: string | null, type: string, data: Record<string, unknown>) {
    this.db
      .prepare(
        "INSERT INTO analytics(audit_id,type,data,created_at) VALUES(?,?,?,?)",
      )
      .run(id, type, JSON.stringify(data), new Date().toISOString());
  }
  claim() {
    return this.transaction(() => {
      if (this.db.prepare("SELECT id FROM jobs WHERE state='RUNNING'").get())
        return null;
      const job = this.db
        .prepare(
          "SELECT * FROM jobs WHERE state IN ('PENDING','RETRYING','WAITING_FOR_RESOURCES') AND available_at<=? ORDER BY priority DESC,created_at LIMIT 1",
        )
        .get(Date.now());
      if (!job) return null;
      this.db
        .prepare(
          "UPDATE jobs SET state='RUNNING',attempts=attempts+1,started_at=? WHERE id=?",
        )
        .run(new Date().toISOString(), job.id);
      this.db
        .prepare("UPDATE audits SET state='RUNNING' WHERE id=?")
        .run(job.audit_id);
      return this.getAudit(String(job.audit_id));
    });
  }
  saveInventory(id: string, inventory: Inventory) {
    this.db
      .prepare("UPDATE audits SET inventory=? WHERE id=?")
      .run(JSON.stringify(inventory), id);
    this.analytics(id, "site.discovered", {
      count: inventory.count,
      wordpress: inventory.wordpress,
      woocommerce: inventory.woocommerce,
    });
  }
  complete(id: string, report: Report) {
    this.transaction(() => {
      for (const page of report.pages) {
        const inserted = this.db
          .prepare("INSERT INTO audit_pages(audit_id,url,kind) VALUES(?,?,?)")
          .run(id, page.url, "selected");
        this.db
          .prepare("INSERT INTO metrics(page_id,data) VALUES(?,?)")
          .run(inserted.lastInsertRowid, JSON.stringify(page));
      }
      for (const issue of report.issues) {
        const inserted = this.db
          .prepare(
            "INSERT INTO issues(audit_id,rule_id,url,data) VALUES(?,?,?,?)",
          )
          .run(id, issue.rule_id, issue.affected_url, JSON.stringify(issue));
        this.db
          .prepare("INSERT INTO recommendations(issue_id,action) VALUES(?,?)")
          .run(inserted.lastInsertRowid, issue.recommendation);
      }
      this.db
        .prepare("INSERT INTO reports VALUES(?,?)")
        .run(id, JSON.stringify(report));
      this.db
        .prepare("UPDATE audits SET state='COMPLETED',report=? WHERE id=?")
        .run(JSON.stringify(report), id);
      this.db
        .prepare(
          "UPDATE jobs SET state='COMPLETED',finished_at=? WHERE audit_id=?",
        )
        .run(new Date().toISOString(), id);
      this.emit(id, "report.ready", { issues: report.issues.length });
      this.analytics(id, "scan.completed", {
        issues: report.issues.map((i) => i.rule_id),
        metrics: report.pages.map((p) => ({
          ttfbMs: p.ttfbMs,
          lighthouse: p.lighthouse,
        })),
      });
    });
  }
  fail(id: string, message: string) {
    this.db
      .prepare("UPDATE audits SET state='FAILED',error=? WHERE id=?")
      .run(message, id);
    this.db
      .prepare("UPDATE jobs SET state='FAILED',finished_at=? WHERE audit_id=?")
      .run(new Date().toISOString(), id);
    this.emit(id, "scan.failed", { message });
    this.analytics(id, "scan.failed", { message });
  }
  wait(id: string) {
    const job = this.db
      .prepare("SELECT resource_waits FROM jobs WHERE audit_id=?")
      .get(id)!;
    if (Number(job.resource_waits) >= 10)
      return this.fail(id, "Resource wait budget exhausted");
    this.db
      .prepare(
        "UPDATE jobs SET state='WAITING_FOR_RESOURCES',attempts=attempts-1,resource_waits=resource_waits+1,available_at=? WHERE audit_id=?",
      )
      .run(Date.now() + 30000, id);
    this.db
      .prepare("UPDATE audits SET state='WAITING_FOR_RESOURCES' WHERE id=?")
      .run(id);
    this.emit(id, "job.waiting_for_resources", {});
  }
  recover() {
    for (const job of this.db
      .prepare("SELECT audit_id FROM jobs WHERE state='RUNNING'")
      .all())
      this.fail(String(job.audit_id), "Worker interrupted; submit a new scan");
  }
  close() {
    this.db.close();
  }
}
