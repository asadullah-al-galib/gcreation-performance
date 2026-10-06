## PURPOSE

Execute the already-authorized operator gate for **TRUSTED CONTROLLER REFRESH ONLY**. REPAIR_1 independent source/security review PASS applies to candidate `134ddfbe393168ce7cef99c44817329c84a8d6eb` only. P1 is incomplete, full-Part review PENDING, repair_cycle1; orchestrator HUMAN_CAPABILITY_GATE. **P0.2§8 grants this exact refresh, subject to all existing verification requirements; its constrained capability is unavailable.** A designated operator may perform these already-approved steps and return proof. Codex may use only an already-approved restricted interface, never raw root/escalation. P0.2§9 grants one REPAIR_1 deployment only after verified refresh; no current request is ready.

## WHY REQUIRED

The consumed deployment of parent `08b395cf08523dbc5ab27f744d174b8a19bb2b4b` failed at non-root-build because UMask0077 masked source directories to0700. Accepted source fixes traversal without relaxing V4 controls. Source review does not prove installed replacement or real runtime success. The reviewer did not directly hash server-local archive bytes: the operator must independently verify the protected copy, every archived file and fresh snapshot before replacing anything.

## EXACT REVIEWED ARTIFACT

- Candidate: `134ddfbe393168ce7cef99c44817329c84a8d6eb`; exactly one parent `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`.
- Existing source DATA: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-134ddfbe393168ce7cef99c44817329c84a8d6eb.tar.gz`. Never execute repository code as root or use mutable workspace files as replacement bytes.
- Archive SHA256: `d2c69e1a49342ae09867bd206e39e89d969c8d0e39eb3c6e9b1eaaf93c1e68b0`; exactly106 regular safe members, including the exact candidate marker.
- Full source manifest SHA256: `b8900ea6c39fa2baf3b3481263e6ef778e3f5eb54fcb019ffb600ca6014d5a95`.
- Expected canonical snapshot digest: `8425d68350e9c9d93f941f62591142cd21a68835b35df188ee63cc415b3054b5`.
- NEW stage only: `/var/lib/gcreation-perf-review/134ddfbe393168ce7cef99c44817329c84a8d6eb`; stage root:root0700; `reviewed-source.tar.gz` and `approved.json` root:root0600; root-owned immutable snapshot. Stage/snapshot must not already exist; if they do, STOP without deletion or reuse.
- Parent controller SHA256: `1a0b509e14777329932771fe5332d05798f368e0788220256b5de9403f72dc54`.
- Candidate controller SHA256: `029c5d5714a13fbdd3565901bdc08341e36319c1ab90cf30ea6d4ab7e58c4039`.
- ONLY installed replacement: `/usr/local/lib/gcreation-perf-dev/deploy_controller.py`, final root:root0644.
- Existing immutable image must remain `sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24`.
- Acceptance: REPAIR_1_ACCEPTANCE.json. Reviewed repair package `runtime-repair-1/` remains unchanged at handoff `e179e19613af37648023f22b495f8fa3b1c3f71c`; its CHECKSUMS.sha256 identity is `0ce4949faca74f32428cdad8682c345598cbb19e02c834be90c8cec66b45c63d`.

## PRECONDITIONS

Master Authorization V2§8 explicitly approves this candidate-only operation with all existing trust checks unchanged. No new approval is requested. The present missing capability requires a designated operator or an already-approved constrained refresh interface; Codex must not create privileges or execute raw root. No runtime deployment/request/health action is included in this refresh operation. Prior INITIAL request1/1 remains consumed, automatic retries0.

Preserve the old failed root stage8217aa4 and accepted installation stage08b395c, failed runtime release, retained DEV networks and their IDs/memberships, old deployment status/evidence, existing source artifact, runtime.env/private receiver env files, immutable image/runtime-image-id, dependency baseline, systemd units, build-context, WordPress/Plesk/nginx and production/main. Do not reset failed service status, enable/restart services, clean caches/evidence, delete releases/networks, rerun install-root.sh or run prepare_image.py/docker build. Existing build-context makes reinstall inappropriate; image/dependency/trusted image inputs are unchanged.

Confirm request and claimed-request files are absent using lstat/no-follow semantics, active release and runtime containers absent, deploy service not running (its existing failed state may remain), watcher active/enabled and no concurrent operator/controller activity. Inspect only whitelisted status/identity fields; never full Docker inspect, argv, Config.Env, secret/config contents or secret-derived hashes in returned evidence. All root paths/ancestors must be root-owned, non-symlink and non-writable by group/other; regular inputs must have link count1. A mismatch stops before replacement, without automatic remediation.

## MINIMUM HUMAN ACTION

Under the already granted P0.2§8 approval: establish one new verified root-only review stage; independently verify archive/map/digest/preflight; prove the installed controller is still the approved parent and other installed components are unchanged; retain a private rollback copy; atomically replace only the controller; verify postconditions. Return sanitized results. After verified refresh, P0.2§9 permits one REPAIR_1 deployment through the existing reviewed watcher, retries0; no extra routine approval is needed. Missing verification/capability still stops; no request before proof.

## SAFE COMMAND/UI STEPS

Future human/operator steps only. Codex must not run these commands.

1. Review `runtime-repair-1/SOURCE_DIFF.patch`, PRIVILEGED_DIFF.patch and the acceptance record. Use the already reviewed **staging-only** system-standard-library DATA bootstrap in `ops/dev/ROOT_TRUST_TRANSITION.md`, with the exact candidate/hash above and clean `env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I -B` startup. The human types/pastes reviewed stdin; do not source/read a repository executable as root. Execute only staging/copy/validation/extraction, never that document's installer block. Reject existing stage/snapshot, unprotected ancestors, unsafe archive copy ownership/mode/link count or any mismatch. Preserve all original stages. Copy only the archive as DATA to the new root-owned0600 archive before trusting bytes.
2. Before extracting, hash that protected copy against the exact archive SHA. Bound compressed/expanded/member bytes as in the reviewed bootstrap; validate all entries before creating files. Require exactly106 unique canonical relative regular members, no links/special entries/traversal/absolute/private credential paths, no `.pyc` or `__pycache__`, and `REVIEW_SOURCE_COMMIT` exactly candidate plus newline. Never use extractall. Compute the complete sorted `sha256(content) + '  ' + relative-name + '\n'` manifest and match the pinned manifest SHA. Compute canonical digest in sorted Path order: relative UTF-8 path, NUL, raw32-byte content SHA256; match the pinned expected snapshot digest. Do not take expected values from developer-writable metadata. If the old staging recipe does not enforce these additional exact-count/manifest/digest/cache checks, the operator must apply them in reviewed system-only stdin before extraction; no replacement may precede them.
3. Extract fresh files as root-owned0644 into the private new snapshot; create root-owned0600 approved.json with exactly the commit, archive SHA and106-entry file-hash map from those verified archive bytes. Independently walk the extracted tree with lstat: reject symlinks/hardlinks/special files, group/other writes, non-root ownership, bytecode/cache entries or extra/missing files. Match every file hash to the verified map; approved.json must equal that map and identities. Recompute manifest/canonical digest from actual extracted bytes. Check archive/stage/approval ownership/modes and root-only access again. Only then may reviewed code in this immutable snapshot execute.
4. Run only the **reviewed installation preflight**, with bytecode disabled, from that new verified snapshot. This performs read-only Docker/systemd/DEV-DNS prerequisites and private environment validation; it does not install, build, enable or deploy. Keep any diagnostic output root-private in the new stage; return only sanitized exit/result, not environment values. Example, under P0.2§8 after completed DATA verification:

   ```sh
   /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I -B \
     /var/lib/gcreation-perf-review/134ddfbe393168ce7cef99c44817329c84a8d6eb/snapshot/ops/dev/install_preflight.py \
     /var/lib/gcreation-perf-review/134ddfbe393168ce7cef99c44817329c84a8d6eb/snapshot \
     d2c69e1a49342ae09867bd206e39e89d969c8d0e39eb3c6e9b1eaaf93c1e68b0 \
     134ddfbe393168ce7cef99c44817329c84a8d6eb
   ```

   Require exit0, exact snapshot/file map/digest after preflight and still no bytecode. Failure stops; no installed replacement, installer rerun, secret adjustment or verifier bypass.
5. Acquire the **existing** root-owned private `/var/lib/gcreation-perf-dev/deploy.lock` exclusively/nonblocking for pre-refresh checks through replacement/verification/rollback. Inspect it and all ancestors without following links; if missing/unsafe/busy, STOP without recreating it or clearing service state. Keep the operator session/lock open. Recheck request/claims absence and service not running; no request may be submitted during this operation.
6. Prove the installed controller is root:root0644, single-link regular, protected by immutable root-owned ancestors, with the exact parent hash above and byte equality to the preserved accepted08b395c root snapshot controller. Independently require that preserved parent controller's hash matches the pinned parent hash; do not assume the old stage is correct merely because it exists. New snapshot controller must have the exact candidate hash. Any other installed controller identity stops for a separate decision; never overwrite unexplained bytes.
7. Before replacement, create a root-private inventory in the new stage of every installed trusted file/directory: content hash, owner/group/mode/type/link count and pathname. Verify OTHER installed reviewed components against unchanged candidate snapshot bytes: deploy-dev.sh0755; runtime.Dockerfile, seccomp_profile.json and install_preflight.py0644; deploy.service/path/slice under /etc/systemd/system0644; all root:root. Verify dependency-baseline.json root:root0644 with exactly the candidate package.json/package-lock.json hashes. Verify build-context's runtime.Dockerfile, both manifests and the nine fixed trusted-source inputs from prepare_image.py against candidate bytes, without executing prepare_image.py. Check installed runtime-image-id and read-only Docker image identity against the pinned existing image; no build/tag/pull. Inventory every other existing trusted entry (including generated cache if present) for unchanged post-comparison; unexpected enforcement modules or unsafe entries stop for review rather than cleanup/acceptance. Privately inventory runtime.env0600, receiver env files, units, build-context, both old stages, failed release, old status/evidence/source artifact and network identities; never print secret values or private config hashes. Establish before/after equality proofs, not invented baseline hashes.
8. Preserve the verified old controller as `controller-before.py` root:root0600 in the new stage, and record its pinned hash in a root-private refresh record. Backup bytes must equal installed parent bytes; do not overwrite an existing backup. Use a new, same-directory root-controlled temporary file under the trusted installed directory, never a workspace file. Confirm the temporary path is absent and its parent immutable/root-owned; hold the lock. The following illustrates the **only** allowed replacement after steps1–7 PASS; the human uses a clean root shell and `set -eu`. These are system utility operations, not execution of repository/snapshot controller code:

   ```sh
   STAGE=/var/lib/gcreation-perf-review/134ddfbe393168ce7cef99c44817329c84a8d6eb
   TRUSTED=/usr/local/lib/gcreation-perf-dev
   test ! -e "$STAGE/controller-before.py" && test ! -L "$STAGE/controller-before.py"
   test ! -e "$TRUSTED/.controller-repair1.tmp" && test ! -L "$TRUSTED/.controller-repair1.tmp"
   test "$(/usr/bin/sha256sum "$TRUSTED/deploy_controller.py" | /usr/bin/cut -d ' ' -f 1)" = 1a0b509e14777329932771fe5332d05798f368e0788220256b5de9403f72dc54
   /usr/bin/install -o root -g root -m 0600 "$TRUSTED/deploy_controller.py" "$STAGE/controller-before.py"
   /usr/bin/cmp -s "$STAGE/controller-before.py" "$TRUSTED/deploy_controller.py"
   /usr/bin/install -o root -g root -m 0644 "$STAGE/snapshot/ops/dev/deploy_controller.py" "$TRUSTED/.controller-repair1.tmp"
   /usr/bin/cmp -s "$TRUSTED/.controller-repair1.tmp" "$STAGE/snapshot/ops/dev/deploy_controller.py"
   test "$(/usr/bin/sha256sum "$TRUSTED/.controller-repair1.tmp" | /usr/bin/cut -d ' ' -f 1)" = 029c5d5714a13fbdd3565901bdc08341e36319c1ab90cf30ea6d4ab7e58c4039
   test "$(/usr/bin/stat -c '%u:%g:%a:%h' "$TRUSTED/.controller-repair1.tmp")" = 0:0:644:1
   /usr/bin/mv -T -- "$TRUSTED/.controller-repair1.tmp" "$TRUSTED/deploy_controller.py"
   ```

   Same-directory mv is an atomic rename on the installed filesystem; precheck that both paths/parents are on the same filesystem and root-controlled. No service restart/reload is needed. `set -e` is insufficient to restore after a failed postcheck: the explicit failure branch in ROLLBACK below is mandatory. Before releasing the lock, verify final installed hash/byte equality/root:root0644/link count1, repeat exact snapshot verification, and compare all non-controller inventories. No other trusted installed bytes/modes may change.
9. Verify unchanged image/dependency baseline/systemd units/build-context/runtime.env and private env files, both old review stages, failed release/networks/status/evidence/source artifact. Read-only watcher active/enabled and deploy service still not running; do not reset its failed state. Request/claims still absent, active release/runtime containers absent, no new deployment occurred. Do not probe runtime health or create a request. Only new review-stage DATA/evidence and the verified controller inode replacement are permitted.
10. Return sanitized checks and explicit controller-refresh exit/result. Release the lock after success or verified rollback. P1 remains incomplete/full review PENDING; repair_cycle stays1. Codex validates and records returned evidence, then executes at most the P0.2-authorized single REPAIR_1 deployment after verification through the reviewed watcher; no retry or P2 before required P1 exit evidence.

## EXPECTED OUTPUT

Fresh stage archive/member/marker/map/manifest/digest/preflight PASS; parent installed hash/baseline comparisons PASS; private backup/hash preserved; ONLY controller replaced atomically with candidate bytes/root:root0644; all other inventory/identity comparisons unchanged; watcher active/enabled; no request/new deployment. This is controller-refresh evidence only, never installation rerun, runtime PASS, D24–D27 completion or full P1 PASS.

## SANITIZED EVIDENCE TO RETURN

Human approval/designated operator, observation times and exact scoped commands/exit codes; protected archive SHA/count/marker/manifest/digest/approved-map/preflight/no-bytecode results; pre/post installed controller hashes/ownership/mode and backup location/hash; unchanged-other-components/image/dependency/units/build-context/environment/stage/release/network/status/artifact attestations; lock held, watcher active/enabled, request/claim absence and zero new deployments. Return no secrets, Config.Env, full inspect, argv, tokens, private configuration hashes or credentials. Missing checks remain PENDING_HUMAN. This gate has not been executed by Codex.

## ROLLBACK

Before atomic replacement, failure means STOP without installed change. Preserve new stage/backup/temporary evidence; do not delete anything or retry. If replacement occurred and ANY verification fails, keep the existing lock and restore ONLY the previous controller atomically from the verified root-private backup: validate backup regular/root:root0600/single-link/pinned parent hash; create a fresh absent root-controlled same-directory temporary rollback file with system install root:root0644; verify its bytes/hash/mode/link count; same-filesystem mv -T over the installed controller. Verify installed parent bytes/root:root0644 and unchanged non-controller inventories, record failure/rollback evidence and STOP. Do not execute either controller or restart services. If restore itself cannot be verified, preserve evidence and stop for a human decision; never claim success. No runtime rollback, status reset or cleanup is part of this gate.

## WHAT CODEX MUST NOT DO

No root/escalation/Docker/systemd/Plesk/nginx/WordPress action, install-root.sh/prepare_image.py/image rebuild, installed controller modification/execution, new root stage creation, source artifact export/copy into watcher input, deploy-dev.request, retry, cleanup or root snapshot/evidence mutation. No production/main/P2. Source security PASS grants none of these actions. STOP at HUMAN_CAPABILITY_GATE; this exact refresh is already approved by P0.2; its missing capability stops execution. One REPAIR_1 deployment is conditional on verified refresh; raw privilege/self-expanded interfaces are forbidden.
