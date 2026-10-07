# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. DEV_HOMEPAGE_HISTORICAL_LOG_ANALYSIS verified handoff SHA256 ff36565d9133061ec4cadbeecf41c2fd35020050c1de4da4b8bc3a94a1e8875e. RESULT=COMPLETE reports zero recognized retained DEV log files, zero homepage GET/error matches and zero Python-urllib homepage requests. DEV log coverage UNAVAILABLE; no coverage rows, status set or first/last request times are supplied. Internal health before homepage NOT_PROVEN; homepage predicate, failed predicate, underlying component and root cause NOT_ESTABLISHED. No health success/failure follows from unavailable log evidence. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; budget exhausted. Analysis changes no source, runtime, privileges, configuration or counters. P2–P7 NOT_STARTED; production/main untouched. Next action: One human/operator metadata-only inventory of /var/www/vhosts/system/dev.gcreation.agency/logs to establish filenames, types, link targets, sizes and retention timestamps after zero recognized files. Maximum 32 entries/8KiB; no log contents, symlink following, runtime action, repair, retry or deployment. Evidence: .ops/reports/P1/REPAIR_2_DEV_HOMEPAGE_LOG_REPORT.md and .ops/reports/P1/REPAIR_2_DEV_HOMEPAGE_LOG_ANALYSIS.json.

Next allowed action: One human/operator metadata-only inventory of /var/www/vhosts/system/dev.gcreation.agency/logs to establish filenames, types, link targets, sizes and retention timestamps after zero recognized files. Maximum 32 entries/8KiB; no log contents, symlink following, runtime action, repair, retry or deployment.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) is a metadata-only inventory of the reported DEV log directory. Historical extraction found no recognized files. P1 remains HARD_BLOCKED; no additional deployment or repair is authorized.
