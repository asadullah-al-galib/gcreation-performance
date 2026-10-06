STATUS:
P1 SECURITY_REVIEW_REQUIRED — MINIMAL REPAIR CANDIDATE ONLY

P0 remains FROZEN / human review PASS. P1 execution IN_PROGRESS / independent review PENDING / repair_cycle0. P2–P7 NOT_STARTED. Preparing this candidate consumes no repair cycle.

FAILING CRITERION: P1-ROOT-01, reviewed snapshot identity during privileged image preparation. Human reports original source 8217aa4a13c0265efd8cb81473dd7f00c68d2c34 / archive ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7: preflight PASS, installer EXIT1, ValueError: Reviewed snapshot content mismatch. Generated snapshot/ops/dev/__pycache__/install_preflight.cpython-36.pyc. Exact partial-host record: reports/P1/security-repair/HOST_FAILURE.json (human attested, not agent inspected).

ROOT CAUSE: prepare_image imports install_preflight before verify_snapshot; -I does not disable import bytecode. Non-privileged fixture reproduces rejection. Proposed source repair adds -B only to the two prepare/seal interpreter invocations; verifier and all other privileged boundaries remain unchanged.

REVIEW PACKAGE: [reports/P1/security-repair/REPORT.md](reports/P1/security-repair/REPORT.md). Candidate source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b; proposed archive SHA 80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929; source manifest SHA 11b0c7507058a4fbd56e12398b96547ed7d2b9724153d05ecd44e747460a28d7; repair-package CHECKSUMS.sha256 file SHA b051cc6a167bd15c313fe7ac5822d95497d7a748cedb4b5a98da2e03d323c912. All are review proposals, not approved installation authority.

NEXT ALLOWED ACTION: Independent security review of this candidate. STOP. A review PASS, if later supplied, still requires separate human approval of fresh-stage recovery/installation. Earlier P1 installation procedure is superseded and must not be executed now. Existing root snapshot and copied installation remain untouched; no bytecode deletion, bypass or in-place snapshot repair.

V4 STATIC SECURITY: Original static design PASS remains historical; this installer-path amendment requires new security review. PRIVILEGED DEV INSTALL: HOLD. No deployment request, runtime installation, root/Docker/systemd/Plesk/nginx/WordPress operation or P2 start by Codex. Production/main untouched.
