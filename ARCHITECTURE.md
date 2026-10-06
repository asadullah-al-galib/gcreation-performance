# Architecture

This is a description of the preserved approved V4 design, not a redesign. Execution authority: PROJECT_TIMELINE.md. Current P0 governance is FROZEN; human review PASS; Accepted installation source security review PASS (source08b395c only); P1 HUMAN_CAPABILITY_GATE (execution IN_PROGRESS / full-Part independent review PENDING); REPAIR_1 independent source/security review PASS / repair_cycle1; P0.2 autonomous authority recorded; P2–P7 NOT_STARTED. V4 static security review PASS; installation gate PASS by human-attested real-host evidence; the INITIAL attempt failed at non-root-build; the single REPAIR_1 request is consumed with runtime-health/RuntimeError failure; REPAIR_1 source/security review PASS; P0.2 authorizes the verified controller-only refresh, but its constrained capability is unavailable; one REPAIR_1 deployment is conditionally authorized after verified refresh. Real deployed acceptance pending, production untouched, P1–P6 advancement follows P0.2 through approved constrained capabilities; P7 is not authorized.

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

Final customer flow: Browser → WordPress nonce/session REST → WordPress PHP → trusted gateway at http://127.0.0.1:3101 with ENGINE_SECRET → internal app with distinct APP_GATEWAY_SECRET. Public nginx exposes only GET /perf-engine/health; audit/order/report/admin/quote/SSE routes are not publicly reverse-proxied. Browser-supplied engine-secret headers are never forwarded. Engine management requires a server-held secret. Opaque report tokens are hashed at rest and combined with order/contact verification. Free scan IDs are not management credentials.

Browser egress uses the reviewed image-baked immutable validating forward proxy that resolves and pins public IPs at connection time; browser and Lighthouse use this proxy. Trusted runtime must prohibit direct browser egress and isolate the host. Loopback reachability for the audit API must not become a scan target. The root kit must never execute repository scripts as root.

SQLite WAL/migrations and a single worker avoid Redis/BullMQ. Payment idempotency uses unique WooCommerce order IDs. Selected-page deep analysis avoids Lighthouse across every discovered URL. Raw browser artifacts are not retained by default.

The unchanged V4 design uses separate FETCH_PROXY_SECRET for the app/fetch bridge, frozen image dependencies and network=none future source builds. App/gateway attach only to the dedicated internal network; only trusted proxy additionally attaches to dedicated egress. No release mount supplies trusted code. Approved hashes/source identity and static evidence are in the historical V4 review bundle; current decisions/observed evidence follow PROJECT_TIMELINE.md and MASTER_EXEC_PLAN.md.

Historically the second/third human reviews refined the original proxy/autonomous PHP design (docs/SECOND_SECURITY_REVIEW_RESULT.md and docs/THIRD_SECURITY_REVIEW_RESULT.md). Human V4 static PASS is now recorded in the P0 request; implementation boundaries remain frozen. The automated root watcher deploys only constrained Node/browser runtime. It atomically renames each request before work and validates both dedicated Docker networks and attached-container identities before container start. WordPress is a separate reviewed commit/hash artifact, applied only after independent human approval as the verified DEV PHP user. Installation crosses the trust boundary through a deterministic approved archive, copied as data, hash-verified and safely extracted into root-owned staging; only that reviewed snapshot supplies privileged executable inputs.
