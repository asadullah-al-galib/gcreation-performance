# Architecture

Preserved approved V4 design; execution authority PROJECT_TIMELINE.md. P0 governance FROZEN / human review PASS; V4 static PASS. Gate A/B/C PASS remain recorded as HUMAN_OPERATOR_ATTESTED_VERIFIED_HANDOFF. The explicitly owner-authorized REPAIR_2 watcher request for source 0ac34ba50ab3192abfe2ae425c4283879484258e / archive 958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced was published exactly once at 2026-10-06T13:31:06.813753+00:00. Exact commit/archive RUNNING was observed, followed by same-commit FAILED at runtime-health, error RuntimeError, rollback=false, observed 2026-10-06T13:32:36.927239+00:00. The FAILED status omits archive_sha256; attribution uses the recorded one-shot sequence, without claiming terminal archive/snapshot or running-image identity. Root cause is NOT_ESTABLISHED. Request and claim are absent. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; two failed repair cycles exhaust the budget. No source/privileged-kit changes, retry, restart, image action, cleanup, post-failure diagnosis or HTTP probes. P2–P7 NOT_STARTED; production/main untouched. Next allowed action: Human decision on exhausted P1 repair budget and failed runtime-health requirement. No further deployment, automatic retry, repair, cleanup or P2 is authorized. Evidence: .ops/reports/P1/REPAIR_2_DEPLOYMENT_ATTEMPT.json and .ops/reports/P1/REPAIR_2_RUNTIME_VALIDATION.json.

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
