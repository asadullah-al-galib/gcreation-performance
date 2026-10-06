STATUS:
P1 HUMAN_CAPABILITY_GATE — ALREADY-AUTHORIZED CONTROLLER REFRESH

AUTHORITY: docs/P0_2_AUTONOMOUS_AUTHORIZATION.md §7–§9 and §34.
CONTROLLER REFRESH AUTHORIZED: YES, subject to every existing gate verification/rollback requirement.
CURRENT DEPLOYMENT REQUEST READY: NO. P0.2 grants one REPAIR_1 attempt only after verified refresh; attempts0/1, retries0. Prior INITIAL attempt consumed.

EXACT BLOCKER: No approved constrained interface available to this agent can verify the fresh root-only snapshot and atomically refresh only the installed controller. Private root paths yield PermissionError errno13. Readable installed controller SHA matches accepted parent08b395c, not accepted candidate134ddfbe. Namespace ownership is not host root-ownership proof.

SMALLEST HUMAN ACTION: Designated human operator performs the already-authorized [TRUSTED_CONTROLLER_REFRESH_GATE.md](reports/P1/TRUSTED_CONTROLLER_REFRESH_GATE.md) and returns its consolidated sanitized verification/rollback evidence. This is a capability gate, not a request to repeat approval. No installer rerun, image build, cleanup, new deployment or WordPress/configuration action is requested.

Accepted source: 134ddfbe393168ce7cef99c44817329c84a8d6eb.
Archive SHA256: d2c69e1a49342ae09867bd206e39e89d969c8d0e39eb3c6e9b1eaaf93c1e68b0.
Manifest SHA256: b8900ea6c39fa2baf3b3481263e6ef778e3f5eb54fcb019ffb600ca6014d5a95.
Expected fresh snapshot: 8425d68350e9c9d93f941f62591142cd21a68835b35df188ee63cc415b3054b5.
Source/security review PASS is unchanged, source/design only; operator archive/map/preflight/parent/unchanged-component verification remains mandatory. Preserve old/fresh stages, failed release, network/status/evidence/source artifact, secrets, image, baseline, units and build-context. Do not reuse or clean old snapshots.

AFTER RESUME: Verify returned refresh proof against the exact gate; only then prepare the P0.2-authorized single candidate-pinned watcher attempt and collect required real DEV health/security/resource/identity/retention evidence. First-runtime restoration proof may remain PENDING under P0.2§19 until a previous runtime exists; do not fabricate PASS. P2 cannot start before remaining P1 technical exits.

P0 FROZEN/human PASS; P1 IN_PROGRESS/full independent review PENDING; repair_cycle1 unchanged; P2–P7 NOT_STARTED. External oversight PENDING is non-blocking. Production/main untouched. No request or privileged/runtime action performed. STOP per §7/§34.

Evidence: [P0_2_CAPABILITY_PREFLIGHT.json](reports/P1/P0_2_CAPABILITY_PREFLIGHT.json).
Oversight: [LATEST_CHECKPOINT.md](oversight/LATEST_CHECKPOINT.md), [LATEST_CHECKPOINT.json](oversight/LATEST_CHECKPOINT.json).
