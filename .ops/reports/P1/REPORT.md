# P1 — Security & DEV Deployment Foundation

Checkpoint: WAITING_FOR_HUMAN. P1 execution IN_PROGRESS; independent review PENDING; repair cycle 0. P0 remains FROZEN / human PASS. P2–P7 NOT_STARTED. No technical failure or security defect is asserted. No installation, deployment request, live health probe or production operation was performed.

Authority: [P0.1](../../../docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md) and [P1 technical criteria](../../../PROJECT_TIMELINE.md). P0.1 setup commit: `5db7fde1e17b1f8097a80bf38881184bb1b88b29`. Tested retained implementation source: `8217aa4a13c0265efd8cb81473dd7f00c68d2c34`; static V4 handoff: `5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d`. The current report/governance commit is a descendant, not a new reviewed installation source.

| Evidence class | Observation | Limit |
| --- | --- | --- |
| IMPLEMENTED | Approved V4 kit, immutable proxy/gateway model and health source retained unchanged. | Presence does not prove real DEV behavior. |
| LOCAL_TESTED | 82 safe archive members /81 Git blobs,78 manifest hashes,30 influencing files, prior validation-log hash; five targeted tests pass. | Data/source integrity and mock contracts only. |
| REAL_DEV_VERIFIED | None at this checkpoint. | D24–D27 and all live containment/rollback criteria remain pending. |
| HUMAN_ATTESTED | Previously supplied P0 human PASS and V4 static PASS. | No installation/runtime attestation supplied. |
| NOT_VERIFIED | Root installation, image/dependency/network/secret/cgroup controls, offline deployment, internal/public health, retention/rollback. | Minimum operator gate in HUMAN_ACTION_REQUIRED.md. |

Reviewed installation DATA artifact remains `.ops/test-artifacts/review-source-8217aa4a13c0265efd8cb81473dd7f00c68d2c34.tar.gz`, SHA-256 `ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7`. Locally expected canonical snapshot digest: `3ba8634a292f04079430f1401cf4c5a84fd77157fe1c25257e88b046a381c378`; no deployed snapshot digest is claimed. The original V4 validation log remains at its unchanged immutable hash; it is referenced, not copied or rerun. All D01–D31 and applicable DEV_ACCEPTANCE rows remain PENDING.

[Criterion-level evidence](EVIDENCE.json), [artifact integrity](ARTIFACT_VERIFICATION.json), [local check procedure](LOCAL_CHECKS.md), [targeted test output](LOCAL_VALIDATION.txt) and [human action](HUMAN_ACTION_REQUIRED.md) are bound by CHECKSUMS.sha256. The checksum manifest excludes itself. Reports retain no authentication values, tokens, contacts or payment credentials.

## Next allowed action

The human reviews/approves the exact V4 artifact and carries out the separate bounded DEV installation/configuration action. Return sanitized installation identity/output and an explicit decision on one constrained DEV deployment of the same source. Codex then resumes P1, prepares the source DATA artifact/request only through the confirmed installed mechanism, observes status/health, and collects the remaining effective runtime/rollback evidence. Any later privileged inspection remains human-only. Human waiting spends no repair cycle. P2 begins only when every P1 technical criterion passes with persisted evidence and all operator/security gates are cleared. Independent review remains PENDING; P6 final handoff stops; P7 requires separate authorization.
