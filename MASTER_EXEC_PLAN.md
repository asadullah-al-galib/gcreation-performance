# Current execution ledger

Authoritative execution order: [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md). Product intent remains [docs/MASTER_PRODUCT_SPEC.md](docs/MASTER_PRODUCT_SPEC.md). The frozen [P0 governance request](docs/P0_GOVERNANCE_FREEZE_REQUEST.md) is narrowly amended for P1–P6 execution by [P0.1](docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md); operator/security gates and independent review remain separate. [REQUIREMENTS.md](REQUIREMENTS.md) is the D01–D31 evidence cross-map; [.ops/PROJECT_STATUS.md](.ops/PROJECT_STATUS.md) is the compact current status.

## Current gate

P0 remains FROZEN / human review PASS at approved governance 1c6303e0c17b04952ee6e9c8b01d6868e53fe152 and freeze record 999ade0ea2695e92c1365a09a3e13f87bd4ef758. P0.1 authorizes sequential P1–P6 technical execution. Current Part P1: execution IN_PROGRESS, workflow WAITING_FOR_HUMAN, independent review PENDING, repair cycle 0. P2–P7 NOT_STARTED. Machine state: .ops/ORCHESTRATOR_STATUS.json. P0.1 grants one bounded P1–P6 execution authorization. Advance sequentially only after full technical exit evidence is persisted, no human/operator action or concrete blocker remains, and V4 boundaries are unchanged. Record EXECUTION_PASS with INDEPENDENT_REVIEW PENDING; Codex never grants human PASS/FROZEN. Stop at WAITING_FOR_HUMAN, SECURITY_REVIEW_REQUIRED, HARD_BLOCKED or P6_REVIEW_READY. P7 needs separate human authorization.

V4 static security: PASS. Privileged DEV installation: HOLD pending separate human/operator installation/configuration. Real DEV/runtime/E2E acceptance is NOT_VERIFIED. Production untouched.

| Part | Completion state | Workflow state | Cycle record                              |
| ---- | ---------------- | -------------- | ----------------------------------------- |
| P0   | FROZEN           | FROZEN         | Human PASS; repair 1/repair 2 not used      |
| P1   | IN_PROGRESS      | WAITING_FOR_HUMAN | Initial cycle; independent review PENDING |
| P2   | NOT_STARTED      | NOT_STARTED    | No cycle started                          |
| P3   | NOT_STARTED      | NOT_STARTED    | No cycle started                          |
| P4   | NOT_STARTED      | NOT_STARTED    | No cycle started                          |
| P5   | NOT_STARTED      | NOT_STARTED    | No cycle started                          |
| P6   | NOT_STARTED      | NOT_STARTED    | No cycle started                          |
| P7   | NOT_STARTED      | NOT_STARTED    | No cycle started                          |

## Preserved baseline and evidence

- Approved implementation source: `8217aa4a13c0265efd8cb81473dd7f00c68d2c34`.
- V4 review handoff: `5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d`.
- Deterministic source archive SHA-256: `ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7`.
- [V4 review bundle](ops/dev/SECURITY_REVIEW_BUNDLE_V4.md): 46 Python, 26 TypeScript and 4 gateway socket tests; PHP/shell/format/lint/typecheck/build/trusted-proxy compilation; offline fresh-source validation;82 regular archive entries and78 immutable source hashes. These are previously recorded local/static results, not tests rerun for P0 or deployed proof.
- Full prior-source validation output is `.ops/test-artifacts/V4_SOURCE_VALIDATION.log`. The bundle records its hash. Retain evidence privately without secrets.
- Original .git is read-only; use scripts/repo-git.sh with .ops/git-metadata. Only develop is committed/pushed. Work stays inside this project.
- P0 changes governance/state Markdown only. Application/runtime/tests/toolchain/privileged kit remain at the accepted baseline. Historical V4 manifests attest the original source archive, not subsequent governance Markdown bytes.

## Approved P0 exit assessment — historical handoff

One fixed eight-Part timeline,32 original milestone assignments and31 acceptance mappings; scope freeze, state machine, two-repair cap, exact handoff/stop rule, human gates and consistent current documentation are prepared for review. P0 verification is limited to diff/content/mapping/unchanged-code checks and clean pushed Git state. Do not run the application suite for this documentation-only Part.

## Approved P0 verification record — historical handoff

The following evidence belongs to the human-approved governance commit 1c6303e0c17b04952ee6e9c8b01d6868e53fe152; it is preserved rather than relabeled as new freeze-transaction validation.

- Documentation formatting and git diff whitespace checks: PASS.
- Timeline coverage:8 Parts with16 required fields each;32/32 milestone intents copied from the unchanged specification and uniquely assigned.
- Acceptance cross-map:31/31 original requirement wordings retained, with owner Part/M0/local evidence/remaining DEV evidence; all DEV_ACCEPTANCE PENDING.
- Current operational documentation consistency:9/9 checked; V4 static PASS, P0 review, installation HOLD, P1 NOT_STARTED and no automatic next-Part execution agree.
- Changed scope:14 governance Markdown files only;72 other baseline files unchanged, including all application/runtime/test/toolchain/privileged kit and historical review artifacts. Original V4 manifest78/78 verified against approved source, not the changed governance tree.
- Historical PROJECT_STATE body and the human governance request text are preserved. No deployment request or privileged/production operation occurred; application suite was not rerun.
- Exact documentation commit, clean working tree and origin/develop equality are verified at final handoff; no self-referencing or guessed commit ID is embedded here.

## Remaining evidence by gate

P1: human-approved controlled installation and actual immutable-image/network/secret/resource/health/deploy/rollback evidence. P2: real controlled browser/Lighthouse/discovery/metrics/rules/jobs/progress/free API evidence. P3: separately approved plugin plus actual customer/session/pricing/DEV checkout evidence. P4: actual idempotent paid audit/secure report/Fix Center/retest/expert/analytics flow. P5: cumulative D01–D29 security/E2E/resource acceptance and D30/D31 release-readiness checks. P6: exact reviewed DEV release candidate, final D30/D31 proof and reconfirmation of all31 criteria. P7: privacy-conscious first 100 consenting DEV customers and measured observations. These Part names describe ordered remaining validation, not missing implementations to rebuild.

## Historical review facts — no current authorization

V2 source 7887fca/handoff 826a622 and V3 source 10dcabfe/handoff 02edd2da were HOLD checkpoints. Their findings and review bundles remain unchanged historical evidence. V4 remediation source 8217aa4/handoff 5c44cb3 preserved prior work and subsequently received human static PASS. Older third/fourth-review stop/install instructions in historical bundles are historical. Current authorization comes from PROJECT_TIMELINE.md as amended by P0.1, not an old continuation or installation recipe.

## Historical P1 preparation checkpoint — superseded by security repair review

P0.1 setup pushed at 5db7fde1e17b1f8097a80bf38881184bb1b88b29. Exact accepted V4 archive/source/manifest/log identities verified;82 members,81 committed blobs,78 manifest hashes and30 influencing files match. Five focused fixture tests PASS. No implementation/kit/dependency/security edits; no real runtime/health/scan/installation or deployment request. [P1 report](.ops/reports/P1/REPORT.md), criterion evidence and checksums record LOCAL_TESTED versus NOT_VERIFIED. D24–D27 remain PENDING_HUMAN; other D/DEV acceptance unchanged. Repair cycle0; no technical failure asserted.

## Current P1 security repair checkpoint

Human installation of original V4 source failed after preflight PASS: EXIT1 / Reviewed snapshot content mismatch, with install_preflight bytecode generated inside the root snapshot. Partial copied files/units exist, build-context/image absent and watcher disabled/inactive, per sanitized human evidence; no agent host inspection. Source repair candidate changes only the two prepare_image interpreter starts to -I -B. Focused regression replays the actual import/verify AST on ordinary-user fixtures; verify_snapshot stays byte-identical and fail-closed. Current package: .ops/reports/P1/security-repair/REPORT.md. Candidate source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b, proposed archive SHA 80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929;50/50 isolated security/bytecode tests PASS; sole privileged diff is two -B flags. Package/manifest hashes are bound in ORCHESTRATOR_STATUS.json. The human now grants independent security PASS for source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b only; acceptance record .ops/reports/P1/SECURITY_REPAIR_ACCEPTANCE.json. V4 boundaries remain accepted; this does not accept the failed snapshot, recovery/installation, runtime or P1 as a whole. The original repair review package is preserved unchanged as review-time evidence.

Next allowed action: separate human/operator approval and fresh-stage recovery per .ops/reports/P1/FRESH_STAGE_OPERATOR_GATE.md. P1 remains execution IN_PROGRESS / full-Part independent review PENDING; repair_cycle0 unchanged. Preserve the failed old stage unchanged; never reuse or clean it. Existing partial installation untouched by Codex; no deployment request, runtime continuation or P2 start. Stop at WAITING_FOR_HUMAN.
