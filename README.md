# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. POST_FAILURE_DIAGNOSTIC_ANALYSIS of the SHA256-verified operator handoff 5d6a17eb8a205bbff38d01adc2aab53d09b3f7daec09ea6bc9afed083a25e128 proves the controller raised RuntimeError: Runtime readiness deadline exceeded at start_runtime line340 after30 aggregate health attempts. Builder exit0, launched container image IDs and preserved failed-source snapshot match accepted inputs by operator evidence; the inner health exceptions are discarded, so the failing endpoint/component and root cause remain NOT_ESTABLISHED. The16-case differential is recorded. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; repair budget exhausted. Analysis performed no runtime/privileged/source/configuration action or counter change. P2–P7 NOT_STARTED; production/main untouched. Next action: One human/operator read-only extraction of retained DEV-only homepage access/error log records for 2026-10-06T13:31:34Z through 13:32:36Z, with coverage/retention and caller-attribution limits. No runtime reproduction, new request, repair, retry or deployment; exhausted budget remains unchanged. Evidence: .ops/reports/P1/REPAIR_2_POSTFAILURE_DIAGNOSTIC_REPORT.md and .ops/reports/P1/REPAIR_2_POSTFAILURE_DIAGNOSTIC_ANALYSIS.json.

Next allowed action: One human/operator read-only extraction of retained DEV-only homepage access/error log records for 2026-10-06T13:31:34Z through 13:32:36Z, with coverage/retention and caller-attribution limits. No runtime reproduction, new request, repair, retry or deployment; exhausted budget remains unchanged.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) is the single proposed historical DEV homepage log extraction. P1 remains HARD_BLOCKED with exhausted repair budget. No additional deployment or repair is authorized.
