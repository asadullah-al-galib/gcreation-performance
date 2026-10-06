STATUS:
P1 SECURITY_REVIEW_REQUIRED — MINIMAL REPAIR CANDIDATE ONLY

P0 remains FROZEN / human review PASS. P1 execution IN_PROGRESS / independent review PENDING / repair_cycle0. P2–P7 NOT_STARTED. Preparing this candidate consumes no repair cycle.

FAILING CRITERION: P1-ROOT-01, reviewed snapshot identity during privileged image preparation. Human reports original source 8217aa4a13c0265efd8cb81473dd7f00c68d2c34 / archive ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7: preflight PASS, installer EXIT1, ValueError: Reviewed snapshot content mismatch. Generated snapshot/ops/dev/__pycache__/install_preflight.cpython-36.pyc. Exact partial-host record: reports/P1/security-repair/HOST_FAILURE.json (human attested, not agent inspected).

ROOT CAUSE: prepare_image imports install_preflight before verify_snapshot; -I does not disable import bytecode. Non-privileged fixture reproduces rejection. Proposed source repair adds -B only to the two prepare/seal interpreter invocations; verifier and all other privileged boundaries remain unchanged.

REVIEW PACKAGE: [reports/P1/security-repair/REPORT.md](reports/P1/security-repair/REPORT.md). Candidate source/archive/manifest identities will be bound at its metadata handoff; no repair approval is implied.

NEXT ALLOWED ACTION: Independent security review of this candidate. STOP. A review PASS, if later supplied, still requires separate human approval of fresh-stage recovery/installation. Earlier P1 installation procedure is superseded and must not be executed now. Existing root snapshot and copied installation remain untouched; no bytecode deletion, bypass or in-place snapshot repair.

V4 STATIC SECURITY: Original static design PASS remains historical; this installer-path amendment requires new security review. PRIVILEGED DEV INSTALL: HOLD. No deployment request, runtime installation, root/Docker/systemd/Plesk/nginx/WordPress operation or P2 start by Codex. Production/main untouched.
