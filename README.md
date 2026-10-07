# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. PROXY_ACCESS_SSL_ANALYSIS verified handoff SHA256 48c9933b7940497980bab554b24fc4fd177b1d0c71d8b4f75f5c3c04af258fae and1144 bytes. The operator reports a56447-byte snapshot mtime2026-10-07T07:53:50Z,246/246 parsed lines,unparsed0; parsed range2026-10-06T22:20:21Z..2026-10-07T07:53:50Z is AFTER readiness window2026-10-06T13:31:34Z..13:32:36Z. In-window requests/GET / matches/Python-urllib GET / all0; status set explicitly NONE; INPUT_BYTES and caller first/last fields absent. CaseA cannot establish either historical predicate. Prior processed SSL overlap/2 parsed requests/0 exact GET / and1 unparsed line remain unchanged; no matching caller/timestamp or cross-layer request/stage identity is established. Watcher attribution/internal health NOT_PROVEN; homepage predicate, failed predicate, component and root cause NOT_ESTABLISHED; no control-flow contradiction demonstrated. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; budget exhausted. No agent protected read, source/runtime/privileged/configuration action or counter change. P2–P7 NOT_STARTED; production/main untouched. Next action: HUMAN DECISION REQUIRED: decide how to address the missing exact historical inner health exception or uniquely watcher-attributable in-window request/error evidence. No further protected-file read is proposed; no repair, retry, runtime reproduction, deployment or repair-budget extension is authorized. Evidence: .ops/reports/P1/REPAIR_2_PROXY_ACCESS_SSL_REPORT.md and .ops/reports/P1/REPAIR_2_PROXY_ACCESS_SSL_ANALYSIS.json.

Next action: HUMAN DECISION REQUIRED: decide how to address the missing exact historical inner health exception or uniquely watcher-attributable in-window request/error evidence. No further protected-file read is proposed; no repair, retry, runtime reproduction, deployment or repair-budget extension is authorized.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) records HUMAN DECISION REQUIRED after insufficient historical evidence. No further file read is proposed or authorized. P1 remains HARD_BLOCKED; no additional deployment or repair is authorized.
