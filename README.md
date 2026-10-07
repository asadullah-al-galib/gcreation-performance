# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. DEV_LOG_DIRECTORY_METADATA_ANALYSIS verified handoff SHA256 bf791778f0fe31c4feec821d4535e71258455c25f88a0ed4bba9b38cf3fd73ac and 1622 bytes. The operator reports an existing readable DEV directory with 8/8 regular entries, no truncation or symlinks. Layout MIXED: access/error candidates and two .processed access equivalents. The prior extractor recognition reason remains NOT_ESTABLISHED; its recognition rules and time-matched file observations are absent. Selected candidate /var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log is regular/nonempty; historical window coverage POTENTIALLY_COVERS_WINDOW, not proven. Internal health before homepage NOT_PROVEN; failed predicate, component and root cause NOT_ESTABLISHED. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; budget exhausted. No protected contents, source, runtime, privileged state, configuration or counters changed. P2–P7 NOT_STARTED; production/main untouched. Next proposal: PROPOSED_SINGLE_FILE_READ — NOT AUTHORIZED: one human/operator read-only extraction from /var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log for 2026-10-06T13:31:34Z..2026-10-06T13:32:36Z, GET / only, maximum 64 rows/16 KiB; sanitize client IPs, headers, user agents, query strings, cookies, tokens, secrets and bodies. No symlink following, other file reads or runtime action. Evidence: .ops/reports/P1/REPAIR_2_DEV_LOGDIR_METADATA_REPORT.md and .ops/reports/P1/REPAIR_2_DEV_LOGDIR_METADATA_ANALYSIS.json.

Next proposal: PROPOSED_SINGLE_FILE_READ — NOT AUTHORIZED: one human/operator read-only extraction from /var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log for 2026-10-06T13:31:34Z..2026-10-06T13:32:36Z, GET / only, maximum 64 rows/16 KiB; sanitize client IPs, headers, user agents, query strings, cookies, tokens, secrets and bodies. No symlink following, other file reads or runtime action.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) records one proposed access-file extraction, explicitly NOT_AUTHORIZED. Metadata collection is complete. P1 remains HARD_BLOCKED; no additional deployment or repair is authorized.
