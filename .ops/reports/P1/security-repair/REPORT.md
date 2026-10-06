# P1 minimal security repair candidate — SECURITY_REVIEW_REQUIRED

Status: REVIEW REQUIRED / INSTALLATION HOLD. P1 execution IN_PROGRESS; independent review PENDING; repair_cycle0 unchanged. This prepares an expressly requested candidate; it grants no repair approval, installation/recovery permission or P1 execution PASS. P0 remains FROZEN; P2–P7 NOT_STARTED. Production/main untouched by this workflow.

## Root cause and real-host evidence

Failing criterion: P1-ROOT-01, approved root snapshot exact identity through image preparation. Original source `8217aa4a13c0265efd8cb81473dd7f00c68d2c34`; archive SHA `ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7`. Human reports initial preflight PASS, installer EXIT1 / `ValueError: Reviewed snapshot content mismatch`, and `snapshot/ops/dev/__pycache__/install_preflight.cpython-36.pyc`. Protected installed files/units copied; build-context and runtime image absent; watcher inactive/disabled; no runtime deployment. [HOST_FAILURE.json](HOST_FAILURE.json) is the exact sanitized HUMAN_ATTESTED record. Codex did not inspect or modify the failed stage or partial installation.

prepare_image.py inserts the reviewed kit directory into sys.path, imports install_preflight, then calls verify_snapshot(). Python -I isolates interpreter environment/search paths but allows import bytecode creation. The import writes a .pyc inside the reviewed snapshot before its actual file map is compared with approved.json. The verifier correctly fails closed on that new file; archive tampering or a weaker verifier is not needed to explain the observed failure.

An ordinary-user Python3.6.8 fixture independently reproduces exactly this sequence and error. The regression executes the actual AST import and verify call from unmodified prepare_image.py and the unchanged verifier, with only fixed review-root/ownership observations substituted for non-root fixtures. It does not execute the full root installer, image preparation/build/seal operations or Docker. No installed/root runtime claim is made.

## Minimal change and security impact

Only two privileged-source lines change in ops/dev/install-root.sh: add -B to prepare_image.py's prepare and seal interpreter starts, retaining -I and every argument. [PRIVILEGED_DIFF.patch](PRIVILEGED_DIFF.patch) is the exact two-line diff against accepted V4. No helper, verifier, archive trust/schema, secret, network, cgroup, SSRF, proxy, gateway, watcher, WordPress or production boundary is changed. No cache deletion, ignore rule, allowlist exception, writable snapshot design or verify_snapshot bypass is introduced. This prevents the demonstrated import side effect at interpreter startup rather than treating the extra file as approved input.

The new focused regression is tests/test_installer_bytecode.py: original -I import must create bytecode and fail; both parsed installer invocations must have exactly -I -B; repaired prepare/seal imports preserve the full approved path/content hash map; both still reject added and modified source, with no __pycache__ created. [V4_BOUNDARIES.json](V4_BOUNDARIES.json) compares50 retained implementation/privileged/influencing files against V4:49 byte-identical, only install-root.sh changed. In particular install_preflight.py (including verify_snapshot), prepare_image.py, manifests, trusted policy/image files and all application/runtime source remain unchanged. Review of this frozen privileged path is still required even though no security check is weakened.

## Tests and limitations

- Targeted original failure reproduction before repair:1/1 PASS (expected child verifier failure confirms the defect).
- Targeted new regression:4/4 PASS.
- Relevant suites in their normal independent processes: deployment12/12, V3 21/21, V4 13/13, new regression4/4 —50/50 PASS; no skipped/removed tests.
- bash -n ops/dev/install-root.sh and git diff whitespace/source-scope assertions: PASS.
- Deterministic archive re-export: identical bytes;105 safe regular members (104 committed blobs plus source marker) all verified against the exact source; complete105-entry source manifest generated.

The initial combined-process50-test run had3 errors: two suites registered different install_preflight modules under one sys.modules key, so deployment mocks patched a replaced module. The complete failing output and diagnosis are retained in [VALIDATION.txt](VALIDATION.txt), followed by the normal isolated commands/results. No runtime/test requirement was changed, weakened, removed or skipped to obtain PASS. This invocation correction is not a source repair or a consumed P1 repair cycle.

These are LOCAL_TESTED fixture/data results. HUMAN_ATTESTED covers the original real-host failure only. REAL_DEV_VERIFIED repair/installation/image/runtime evidence is absent. D24–D27 and all later DEV acceptance remain pending; the existing failure is recorded rather than overwritten as successful acceptance.

## Candidate source and checksum identities

- Candidate source commit: `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`; parent `ba7046f2f2adf30e5382700ea84655aa7e747bae`.
- Proposed deterministic archive: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-08b395cf08523dbc5ab27f744d174b8a19bb2b4b.tar.gz`.
- Proposed archive SHA-256: `80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929`.
- [SOURCE_MANIFEST.sha256](SOURCE_MANIFEST.sha256): every105 source archive member, including REVIEW_SOURCE_COMMIT; manifest file SHA `11b0c7507058a4fbd56e12398b96547ed7d2b9724153d05ecd44e747460a28d7`.
- Expected candidate snapshot digest: `867f258b5bb1261317caa6f601becbb4c7294569ff3b5bc4903d95f926f98fc3` — locally calculated DATA identity, not an observed installed snapshot.
- [ARCHIVE_VERIFICATION.json](ARCHIVE_VERIFICATION.json) binds counts, source/archive/manifest identities and limitations.
- [CHECKSUMS.sha256](CHECKSUMS.sha256) binds all repair-package files except itself; its file SHA is recorded outside the bound set in .ops/ORCHESTRATOR_STATUS.json / .ops/ACTION_REQUIRED.md, avoiding self-reference.

The source commit and archive are proposals, not a new human-approved baseline. The review metadata is a later develop child, excluded from the source archive to avoid self-reference. The original V4 archive and manifests remain intact historical evidence; they do not attest the new installer bytes. The archive is ordinary-user-exported committed DATA; root installation may use only its independently approved, verified root-owned copy/snapshot, never current repository code. It is privately available at the project-local path; a reviewer without that DATA must obtain it or reproduce it unprivileged before approving the archive.

## Exact changed-file inventory and diff

Only the installer and new test change executable/source behavior. The remaining edits record the actual failure/security gate, supersede the obsolete installation action and synchronize explicit current-state lines; historical chronology, M0/D criteria, P0 baseline, old evidence and other code are preserved.

Candidate source commit changes:

- `.ops/ACTION_REQUIRED.md`
- `.ops/ORCHESTRATOR_STATUS.json`
- `.ops/PROJECT_STATE.md`
- `.ops/PROJECT_STATUS.md`
- `.ops/reports/P1/CHECKSUMS.sha256`
- `.ops/reports/P1/EVIDENCE.json`
- `.ops/reports/P1/HUMAN_ACTION_REQUIRED.md`
- `.ops/reports/P1/REPORT.md`
- `.ops/reports/P1/security-repair/HOST_FAILURE.json`
- `.ops/reports/P1/security-repair/VALIDATION.txt`
- `ARCHITECTURE.md`
- `MASTER_EXEC_PLAN.md`
- `PLANS.md`
- `PROJECT_TIMELINE.md`
- `README.md`
- `REQUIREMENTS.md`
- `ROADMAP.md`
- `SECURITY.md`
- `docs/DEV_VALIDATION_RUNBOOK.md`
- `ops/dev/install-root.sh`
- `tests/test_installer_bytecode.py`

Review-metadata child additions/updates:

- `.ops/reports/P1/security-repair/REPORT.md`
- `.ops/reports/P1/security-repair/EVIDENCE.json`
- `.ops/reports/P1/security-repair/CHECKSUMS.sha256`
- `.ops/reports/P1/security-repair/SOURCE_MANIFEST.sha256`
- `.ops/reports/P1/security-repair/SOURCE_DIFF.patch`
- `.ops/reports/P1/security-repair/PRIVILEGED_DIFF.patch`
- `.ops/reports/P1/security-repair/V4_BOUNDARIES.json`
- `.ops/reports/P1/security-repair/CHANGED_FILES.json`
- `.ops/reports/P1/security-repair/ARCHIVE_VERIFICATION.json`
- `.ops/reports/P1/security-repair/RECOVERY_REVIEW.md`
- `.ops/ORCHESTRATOR_STATUS.json`
- `.ops/ACTION_REQUIRED.md`
- `MASTER_EXEC_PLAN.md`

[CHANGED_FILES.json](CHANGED_FILES.json) is the machine-readable inventory. [SOURCE_DIFF.patch](SOURCE_DIFF.patch) is the complete source-commit diff versus its parent, including governance/test/evidence edits, generated with --binary --unified=0. Zero context preserves every change while avoiding whitespace-only blank context records in the saved artifact. The first metadata commit retained those context records and failed its whitespace check; this metadata-only follow-up corrects that artifact, without changing candidate source/archive or test results. This metadata child introduces no executable/privileged-source change; its diff is separately reviewable in Git. It cannot embed its own guessed commit ID.

## Fresh-stage recovery and existing partial install

[RECOVERY_REVIEW.md](RECOVERY_REVIEW.md) specifies a future separately approved human procedure. Preserve the contaminated old root stage as evidence; do not delete its cache, edit approved.json or rerun it. Preserve copied installed files/units and secret configuration. Human verifies their scoped ownership/hashes and the reported inactive/disabled/no-build/no-image state; unexpected state stops recovery. After independent security PASS and separate operator approval, bootstrap a fresh root-only stage for the new commit/hash with unchanged system-only DATA copy/verification/extraction, then run the reviewed installer solely from that new verified snapshot. Same-byte existing installed files/units can remain and be recopied by that approved installer; no blanket cleanup or in-place old-snapshot repair is proposed. No such recovery has been performed.

## Stop

Independent human/security review REQUIRED. No root/Docker/systemd/Plesk/nginx/WordPress operation, partial-install mutation, deployment request, runtime continuation or P2 start by Codex. Production untouched. Local tests do not approve this candidate or installed behavior. Stop at SECURITY_REVIEW_REQUIRED.
