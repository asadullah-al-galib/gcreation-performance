# Architecture

A modular monolith: WordPress/WooCommerce owns sales and payment truth; Fastify owns audit jobs, SQLite, discovery, browser measurements and SSE; deterministic rules own explanation; the plugin presents the HTML Fix Center.

- apps/audit-service: loopback-only API, worker, migrations and persistence.
- packages/contracts: typed evidence, metrics and job interfaces.
- packages/shared: URL/SSRF policy, tokens and centrally configured pricing.
- packages/discovery: bounded same-origin sitemap/link inventory and classification.
- packages/scanner: Playwright and Lighthouse adapters, one heavy job at a time.
- packages/metrics: observed-only normalization.
- packages/rules: centrally testable thresholds and evidence-backed recommendations.
- packages/report-engine: health summary, fixes and comparison.
- wordpress/gcreation-performance: sales UI, authorized gateway, WooCommerce integration, reports and operations.

Final customer flow: Browser → WordPress nonce/session REST → WordPress PHP → http://127.0.0.1:3101 with the server-held secret. Public nginx exposes only GET /perf-engine/health; audit/order/report/admin/quote/SSE routes are not publicly reverse-proxied. Browser-supplied engine-secret headers are never forwarded. Engine management requires a server-held secret. Opaque report tokens are hashed at rest and combined with order/contact verification. Free scan IDs are not management credentials.

Browser egress uses a validating forward proxy that resolves and pins public IPs at connection time; browser and Lighthouse use this proxy. Trusted runtime must prohibit direct browser egress and isolate the host. Loopback reachability for the audit API must not become a scan target. The root kit must never execute repository scripts as root.

SQLite WAL/migrations and a single worker avoid Redis/BullMQ. Payment idempotency uses unique WooCommerce order IDs. Selected-page deep analysis avoids Lighthouse across every discovered URL. Raw browser artifacts are not retained by default.

Version decisions and deployment evidence are recorded in MASTER_EXEC_PLAN.md and ops/dev/README.md.

The second human security review supersedes the original proxy and autonomous PHP deployment design (docs/SECOND_SECURITY_REVIEW_RESULT.md). The automated root watcher deploys only constrained Node/browser runtime. It atomically renames each request before work and validates the exact internal Docker network before container start. WordPress is a separate reviewed commit/hash artifact, applied only after independent human approval as the verified DEV PHP user. Installation crosses the trust boundary through a deterministic approved archive, copied as data, hash-verified and safely extracted into root-owned staging; only that reviewed snapshot supplies privileged executable inputs.
