# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance: FROZEN; human review PASS for approved commit 1c6303e0c17b04952ee6e9c8b01d6868e53fe152. P1 WAITING_FOR_HUMAN (execution IN_PROGRESS / independent review PENDING under P0.1); P2–P7: NOT_STARTED. V4 static security review: PASS for source 8217aa4a13c0265efd8cb81473dd7f00c68d2c34/handoff 5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d, as supplied by the human. Static design approval is not deployed acceptance. Privileged DEV installation remains HOLD pending separate human/operator installation/configuration; browser/Lighthouse/WordPress/WooCommerce/E2E remain pending.

Next allowed action: human action in .ops/reports/P1/HUMAN_ACTION_REQUIRED.md. Independent review alone grants human PASS/FROZEN. Sequential P1–P6 execution follows docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md; independent review remains PENDING, operator/security gates require a stop, and P7 requires separate human authorization. P0 is frozen. P0.1 changes governance only; it grants bounded technical execution without changing the V4 implementation.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) is the separately approved P1 human installation/configuration gate; P0.1 grants preparation, not agent privilege. [V4 DEV kit](ops/dev/README.md) and its archived review recipes are historical/static design evidence; they do not start P1 or authorize installation. Codex never executes root/Docker/systemd/Plesk/WordPress installation or production operations. Later privileged human actions require separate explicit approval. Scope freeze and maximum two repair cycles are defined in the timeline.
