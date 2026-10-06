STATUS:
P1 WAITING_FOR_HUMAN — TRUSTED CONTROLLER REFRESH ONLY

REPAIR_1 INDEPENDENT SOURCE/SECURITY REVIEW: PASS for134ddfbe393168ce7cef99c44817329c84a8d6eb, exact parent08b395cf08523dbc5ab27f744d174b8a19bb2b4b. Accepted scope is source/security design only: no installation, controller refresh, deployment, runtime or full P1 PASS. Record: [reports/P1/REPAIR_1_ACCEPTANCE.json](reports/P1/REPAIR_1_ACCEPTANCE.json). Reviewed runtime-repair-1 package remains unchanged.

ACTION FILE: [reports/P1/TRUSTED_CONTROLLER_REFRESH_GATE.md](reports/P1/TRUSTED_CONTROLLER_REFRESH_GATE.md).
NEXT ALLOWED ACTION: Separate human approval/operator gate for NEW root-only reviewed snapshot and ONLY atomic installed deploy_controller.py refresh to root:root0644, with private parent rollback copy and unchanged-other-component proof. No authorization granted by this source-review acceptance. Reviewer did not directly hash server archive bytes: before replacement reverify protected archive SHA d2c69e1a49342ae09867bd206e39e89d969c8d0e39eb3c6e9b1eaaf93c1e68b0,106 safe members/exact marker/approved file map/manifest SHA b8900ea6c39fa2baf3b3481263e6ef778e3f5eb54fcb019ffb600ca6014d5a95/canonical snapshot8425d68350e9c9d93f941f62591142cd21a68835b35df188ee63cc415b3054b5 and reviewed preflight. No symlinks/hardlinks/special entries or bytecode; installed parent bytes must match08b395c before replacement.

Keep repair_cycle1; P1 execution IN_PROGRESS / incomplete; full independent review PENDING; P0 FROZEN / human PASS; P2–P7 NOT_STARTED. Existing installation/source08b395c PASS is historical installation-only evidence. Prior runtime attempt FAILED/non-root-build with request1/1 consumed, retries0 and rollback=false because no prior runtime. Runtime/health/effective containment/rollback/retention and D24–D27 pending.

CONTROLLER REFRESH AUTHORIZED: NO.
DEPLOYMENT AUTHORIZED: NO.
No install-root.sh rerun, image rebuild, deploy-dev.request, second attempt, reset-failed, cleanup or runtime action. Preserve old/fresh stages, failed release, networks/status/evidence/source artifact/runtime.env/image/baseline/units/build-context/WordPress/Plesk/nginx and production/main. A later successful separately approved refresh must return to WAITING_FOR_HUMAN for a NEW separately approved single deployment gate. Codex performs no privileged action. STOP.
