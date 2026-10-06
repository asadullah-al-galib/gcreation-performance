# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. Gate A/B/C PASS remain recorded as HUMAN_OPERATOR_ATTESTED_VERIFIED_HANDOFF. The explicitly owner-authorized REPAIR_2 watcher request for source 0ac34ba50ab3192abfe2ae425c4283879484258e / archive 958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced was published exactly once at 2026-10-06T13:31:06.813753+00:00. Exact commit/archive RUNNING was observed, followed by same-commit FAILED at runtime-health, error RuntimeError, rollback=false, observed 2026-10-06T13:32:36.927239+00:00. The FAILED status omits archive_sha256; attribution uses the recorded one-shot sequence, without claiming terminal archive/snapshot or running-image identity. Root cause is NOT_ESTABLISHED. Request and claim are absent. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2; INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; automatic retries0; two failed repair cycles exhaust the budget. No source/privileged-kit changes, retry, restart, image action, cleanup, post-failure diagnosis or HTTP probes. P2–P7 NOT_STARTED; production/main untouched. Next allowed action: Human decision on exhausted P1 repair budget and failed runtime-health requirement. No further deployment, automatic retry, repair, cleanup or P2 is authorized. Evidence: .ops/reports/P1/REPAIR_2_DEPLOYMENT_ATTEMPT.json and .ops/reports/P1/REPAIR_2_RUNTIME_VALIDATION.json.

Next allowed action: Human decision on exhausted P1 repair budget and failed runtime-health requirement. No further deployment, automatic retry, repair, cleanup or P2 is authorized.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) is a decision on the exhausted P1 repair budget after REPAIR_2 failed at runtime-health. No additional deployment or repair is authorized; Codex retains no unrestricted privilege.
