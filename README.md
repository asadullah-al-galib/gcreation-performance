# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance: FROZEN; human review PASS for approved commit 1c6303e0c17b04952ee6e9c8b01d6868e53fe152. Accepted installation source security review PASS (source08b395c only); P1 HUMAN_CAPABILITY_GATE (execution IN_PROGRESS / full-Part independent review PENDING); REPAIR_1 independent source/security review PASS / repair_cycle1; P0.2 autonomous authority recorded; P2–P7: NOT_STARTED. V4 static security review: PASS for source 8217aa4a13c0265efd8cb81473dd7f00c68d2c34/handoff 5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d, as supplied by the human. Static design approval is not deployed acceptance. Installation gate PASS by human-attested real-host evidence; the INITIAL attempt failed at non-root-build; the single REPAIR_1 request is consumed with runtime-health/RuntimeError failure; REPAIR_1 source/security review PASS; P0.2 authorizes the verified controller-only refresh, controller refresh PASS is recorded from complete operator proof and independent read-only identity checks; one REPAIR_1 deployment is conditionally authorized after verified refresh; browser/Lighthouse/WordPress/WooCommerce/E2E remain pending.

Next allowed action: Provide preserved failing health-probe exception or pre-cleanup container startup evidence if available; otherwise a human decision on a bounded diagnostic approach is required. No unchanged retry or REPAIR_2 attempt. No routine approval requested; continue only within P0.2 capabilities and required technical exits.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) tracks current P1 acceptance/capability requirements; no new approval is requested; installation is verified by supplied operator evidence, and Codex retains no privilege. [V4 DEV kit](ops/dev/README.md) and its archived review recipes are historical/static design evidence; they do not start P1 or authorize installation. Codex never executes root/Docker/systemd/Plesk/WordPress installation or production operations. Later privileged human actions require separate explicit approval. Scope freeze and maximum two repair cycles are defined in the timeline.
