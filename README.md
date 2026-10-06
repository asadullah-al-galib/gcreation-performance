# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. Authorized DEV: https://dev.gcreation.agency. Production is out of scope and untouched.

Start with [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md), the single authoritative execution order, then [current ledger](MASTER_EXEC_PLAN.md), [compact status](.ops/PROJECT_STATUS.md), [product specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance cross-map](REQUIREMENTS.md) and [durable rules](AGENTS.md). Original M0.1–M0.32 and D01–D31 are preserved; the later [P0 human governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) controls execution gates.

## Current checkpoint

P0 governance FROZEN / human review PASS; V4 static PASS. Gate A/B/C PASS recorded as HUMAN_OPERATOR_ATTESTED_VERIFIED_HANDOFF. Promoted image sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a and Dockerfile SHA256 21ee8641969bc2eb92a91d1dcde28ed90e6420433bb022f1a25d1237c7eec152 match the accepted candidate. Backups, promotion order, unchanged controller, retained old/rejected images and watcher state are operator-attested. Official runtime not started; REPAIR_2 runtime acceptance PENDING. Codex performed no privileged/runtime action. P1 IN_PROGRESS / full independent review PENDING; HUMAN_CAPABILITY_GATE; INITIAL consumed; last consumed runtime repair_cycle1; REPAIR_1 failed/consumed1/1; REPAIR_2 deployment0/1; automatic retries0; P2–P7 NOT_STARTED; production/main untouched. Next allowed action: Human independent authorization of exactly one candidate-pinned REPAIR_2 DEV deployment. No automatic retry. No deployment request is authorized by this checkpoint. Evidence: .ops/reports/P1/REPAIR_2_GATE_C_VERIFICATION.json.

Next allowed action: Human independent authorization of exactly one candidate-pinned REPAIR_2 DEV deployment. No automatic retry. No deployment request is authorized by this checkpoint.

## Existing development foundation — reference, not a P0 execution request

Pinned Node 24.21.0/TypeScript and package-lock.json are preserved; host Node 26/Plesk npm is not the validated runtime. Existing project-local wrappers scripts/bootstrap-toolchain.sh and scripts/npm-dev.sh provide six standard npm quality commands when a later authorized Part needs them. Caches, local SQLite and evidence stay in ignored .ops directories. Do not run Chromium outside the reviewed isolated runtime or add infrastructure/features under the frozen MVP scope.

Approved V4 design: WordPress PHP holds ENGINE_SECRET and calls the trusted localhost gateway; the gateway forwards a distinct APP_GATEWAY_SECRET to the internal app. App/proxy share only scoped FETCH_PROXY_SECRET, and the immutable trusted proxy is the sole dedicated-egress member. Future mutable builds run offline against frozen image dependencies. Public nginx exposes only GET health. Real behavior must be validated under the timeline's P1–P5 gates; local tests inject controlled measurements and never prove unrelated live-site safety or deployed success.

## Git and human actions

Original .git is read-only. scripts/repo-git.sh uses preserved writable metadata at .ops/git-metadata. Commit/push only develop; never modify main or reset valid history. Develop only inside /home/codexperf/projects/gcreation-performance.

[Current human action](.ops/ACTION_REQUIRED.md) is independent authorization of one candidate-pinned REPAIR_2 DEV deployment. Promotion evidence grants no deployment request permission. No automatic retry; Codex retains no unrestricted privilege.
