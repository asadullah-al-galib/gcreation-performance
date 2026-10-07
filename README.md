# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. ACCESS_SSL_SINGLE_FILE_ANALYSIS verified handoff SHA256 138a8a5536ec37a9875e6534a19f0a30618895b63caa3ba7319786af64b9d9c5 and 1073 bytes. The operator reports 53/53 parsed access lines, unparsed0, spanning2026-10-07T00:23:53Z..2026-10-07T06:48:33Z, entirely AFTER the2026-10-06T13:31:34Z..13:32:36Z readiness window. In-window requests/GET / matches/Python-urllib matches0; status set explicitly NONE; Python-urllib first/last timestamps absent. CaseA cannot establish a historical predicate. Watcher attribution and internal health NOT_PROVEN; DEV homepage predicate, failed predicate, component and root cause NOT_ESTABLISHED. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; budget exhausted. No agent protected contents, source, runtime, privileged state, configuration or counter action. P2–P7 NOT_STARTED; production/main untouched. Next proposal: PROPOSED_NEXT_SINGLE_EVIDENCE_READ — NOT AUTHORIZED: one future human/operator extraction from /var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log.processed for 2026-10-06T13:31:34Z..2026-10-06T13:32:36Z, GET / only, maximum 64 rows/16 KiB; sanitize client IPs, headers, raw user agents, query strings, cookies, tokens, secrets and bodies. No symlink following, other file read or runtime action. Evidence: .ops/reports/P1/REPAIR_2_ACCESS_SSL_SINGLE_FILE_REPORT.md and .ops/reports/P1/REPAIR_2_ACCESS_SSL_SINGLE_FILE_ANALYSIS.json.

Next proposal: PROPOSED_NEXT_SINGLE_EVIDENCE_READ — NOT AUTHORIZED: one future human/operator extraction from /var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log.processed for 2026-10-06T13:31:34Z..2026-10-06T13:32:36Z, GET / only, maximum 64 rows/16 KiB; sanitize client IPs, headers, raw user agents, query strings, cookies, tokens, secrets and bodies. No symlink following, other file read or runtime action.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) records one next processed-access-file read, explicitly NOT_AUTHORIZED. Current access_ssl_log parsed timestamps are after the failure window. P1 remains HARD_BLOCKED; no additional deployment or repair is authorized.
