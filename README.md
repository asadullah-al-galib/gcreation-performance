# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. State HUMAN_CAPABILITY_GATE. Independent security review PASS recorded for exact patch1bfe3e0c; approved runtime.Dockerfile three-directory offline chmod implemented. Candidate 0ac34ba50ab3192abfe2ae425c4283879484258e passes exact-archive source regression (59 Python,26 TypeScript,4 gateway;16 commands exit0). New image NOT_BUILT; actual root-owned image/UID10001 positive and root0700 negative acceptance PENDING_HUMAN. P1 IN_PROGRESS / full independent review PENDING; last consumed runtime repair_cycle1, REPAIR_1 failed/consumed1/1, REPAIR_2 deployment0/1, retries0, INITIAL consumed; P2–P7 NOT_STARTED; production/main untouched. Next allowed action: Human review and explicit authorization/execution of the constrained fresh-image upgrade gate ops/dev/REPAIR_2_IMAGE_UPGRADE_GATE.md; no deployment request/image/promotion by Codex. Evidence: .ops/reports/P1/runtime-repair-2/REPORT.md.

Next allowed action: Human review and explicit authorization/execution of the constrained fresh-image upgrade gate ops/dev/REPAIR_2_IMAGE_UPGRADE_GATE.md; no deployment request/image/promotion by Codex.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) is the proposed constrained fresh-image upgrade gate; source PASS does not authorize image build/promotion. Codex retains no privilege. Archived review/installation recipes grant no new permission; scope freeze and two-repair maximum remain.
