## PURPOSE

SUPERSEDED — DO NOT EXECUTE. These commands describe the failed old-source gate only; its contaminated snapshot must never be reused or cleaned. Current P1 state BLOCKED / REPAIR_1 REVIEW_READY, orchestrator SECURITY_REVIEW_REQUIRED. Installation verified by INSTALLATION_EVIDENCE.json; subsequent deployment gate consumed/FAILED. Current action is runtime-repair-1/HUMAN_REVIEW_GATE.md; no installation or request authorized now.

Review and separately approve the exact retained V4 artifact, then manually install/configure the reviewed DEV foundation so P1 can validate real containment. Current state WAITING_FOR_HUMAN; no DEV installation/runtime acceptance is claimed.

## WHY REQUIRED

Root staging, Docker/image/systemd installation, root-private configuration and DEV nginx are human/operator actions. P0.1 grants Codex preparation and sequential technical execution only, not those privileges. The human static V4 PASS and the umbrella execution authorization do not constitute installation or effective-runtime evidence. No repair cycle is consumed by this wait.

## EXACT REVIEWED ARTIFACT

- Installation source commit: `8217aa4a13c0265efd8cb81473dd7f00c68d2c34`.
- Static V4 handoff: `5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d`.
- DATA archive: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-8217aa4a13c0265efd8cb81473dd7f00c68d2c34.tar.gz`.
- Human-approved archive SHA-256: `ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7`.
- V4 manifest: `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_SHA256SUMS_V4` (78 entries attest the original archive).
- Preserved bootstrap recipe: `/home/codexperf/projects/gcreation-performance/ops/dev/ROOT_TRUST_TRANSITION.md`, identical to the archived source.
- Preserved installer/nginx inputs: `ops/dev/install-root.sh` and `ops/dev/nginx-dev.conf.example` inside that archive.
- Local DATA verification: ARTIFACT_VERIFICATION.json; expected snapshot digest `3ba8634a292f04079430f1401cf4c5a84fd77157fe1c25257e88b046a381c378` is local only.

Use this exact archived source for installation. The P0.1/report commit is governance metadata, not a replacement privileged artifact. Archived HOLD text describes its earlier review checkpoint; current authority is the recorded static PASS plus your separate present installation decision.

## PRECONDITIONS

- Human independently reviews the exact archive/hash and bootstrap recipe, then explicitly approves this DEV-only operator action. If not approved, leave installation HOLD.
- Human controls the DEV host and verifies Docker with systemd cgroup driver, BuildKit, x86_64 and systemd>=239. Missing prerequisites require a human decision; do not expand host/security scope automatically.
- No deployment request, including a dangling symlink, exists. Do not clear unexplained requests or replace an existing staging/build context automatically; stop and return exact sanitized evidence if one exists.
- Root staging/protected ancestors are root-owned, symlink-free and not writable by codexperf. This source has not already been partially installed; if it has, report existing identity/state before rerunning the non-idempotent bootstrap.
- Human provisions root-owned mode0600 `/etc/gcreation-perf-dev/runtime.env` privately with three distinct documented secrets and DENIED_IPS covering103.112.63.86 plus every current public DEV DNS answer. Never return its contents or secret hashes.
- Only the DEV subscription/server block is in scope; production/main/WordPress/WooCommerce remain untouched. No live payment or customer-site scan is requested.

## MINIMUM HUMAN ACTION

After explicit operator approval, stage this exact archive as root-private DATA, verify its separately approved hash, safely extract it using the preserved system-only bootstrap, execute the installer solely from the verified root-owned reviewed snapshot, and apply only the reviewed health-only location to the DEV nginx configuration. Return the installation identity checks below. Also explicitly approve or decline one constrained DEV deployment of the same reviewed source through the installed watcher; no request exists now. Do not deploy PHP or configure WooCommerce during P1.

## SAFE COMMAND/UI STEPS

These are human-only review/install steps. Codex executes none of them. There is no safe single install command because private configuration, verified root staging and DEV-only nginx review are separate gates.

1. Independently verify DATA with the system utility:

   ```sh
   /usr/bin/sha256sum /home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-8217aa4a13c0265efd8cb81473dd7f00c68d2c34.tar.gz
   ```

   Require exactly the archive hash above. Do not derive approval from mutable developer metadata.
2. Open the preserved ROOT_TRUST_TRANSITION.md as text. Manually use its system-only root bootstrap with `COMMIT='8217aa4a13c0265efd8cb81473dd7f00c68d2c34'` and `APPROVED_SHA='ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7'`. Preserve env -i, fixed PATH, Python -I, ownership/hash/entry checks and fail-closed fresh staging. Do not source/execute that repository document or generate root stdin from repository bytes. It must copy DATA, rehash the root-owned copy, extract only safe regular members and bind approved.json before any installer execution.
3. Privately provision runtime.env as described under PRECONDITIONS. Once the reviewed root snapshot and preflight inputs are ready, the separately approved installer invocation is:

   ```sh
   /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /bin/bash /var/lib/gcreation-perf-review/8217aa4a13c0265efd8cb81473dd7f00c68d2c34/snapshot/ops/dev/install-root.sh ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7 8217aa4a13c0265efd8cb81473dd7f00c68d2c34
   ```

   It may execute only that root-owned verified snapshot. It must complete with exit0; failed preflight is a stop, not permission to bypass checks.
4. Through the human-controlled DEV nginx/Plesk configuration, apply only `nginx-dev.conf.example` from the verified snapshot to dev.gcreation.agency. Review the existing DEV configuration and use its normal configuration-test/reload procedure; do not modify any production or unrelated server block. The template exposes only GET health; other engine routes404. Health200 is expected only after a later approved runtime deployment.
5. Inspect only scoped non-secret identity/ownership data. Examples:

   ```sh
   /usr/bin/systemctl is-active gcreation-perf-dev-deploy.path
   /usr/bin/stat -c '%U:%G %a %n' /etc/gcreation-perf-dev/runtime.env /usr/local/lib/gcreation-perf-dev/deploy_controller.py /usr/local/lib/gcreation-perf-dev/deploy-dev.sh /usr/local/lib/gcreation-perf-dev/runtime-image-id /usr/local/lib/gcreation-perf-dev/dependency-baseline.json
   /usr/bin/cat /usr/local/lib/gcreation-perf-dev/runtime-image-id /usr/local/lib/gcreation-perf-dev/dependency-baseline.json
   ```

   Never print runtime.env, split env contents, full docker inspect, nginx credential configuration or private journals. Confirm installed component hashes against corresponding archive members and root snapshot ownership/hash verification. Report how these checks were made and their actual exit codes, not only an installation claim.

## EXPECTED OUTPUT

Archive hash matches; fresh reviewed root copy/snapshot verifies; installer exits0; immutable root-owned installed inputs and image sha256 ID plus two frozen dependency hashes are recorded; watcher path active with no stale trigger; human confirms DEV-only nginx test/reload success. No running application or health200 is assumed before a deployment. Runtime networks/split envs/cgroups/build/rollback require subsequent observations after the separately approved deployment; P1 remains incomplete until all criterion-level evidence passes.

## SANITIZED EVIDENCE TO RETURN

Return timestamp, installation decision, exact source/archive identity, actual command exit codes, root snapshot/installed ownership and hash-check summary, immutable image ID, installed dependency-baseline hashes, Docker/systemd/BuildKit capability confirmation, watcher active/no-stale-request result and DEV-only nginx approval/test result. Attest secret distinction/mode/receivers and verified current-DNS self-deny without returning values, hashes of secrets or configuration contents. Explicitly say whether one watcher deployment of this source and DEV-only health probes are approved. Confirm production/main/WordPress/WooCommerce untouched. If already installed, return this evidence instead of reinstalling. You may reply in chat or supply sanitized non-executable evidence under `.ops/reports/P1/`; a marker alone never proves installed/runtime acceptance. Do not include cookies, report tokens, contacts, payment credentials or keys.

## ROLLBACK

On a failed bootstrap/preflight/build/install, stop and report the exact stage/exit code. Do not rerun or delete an existing protected stage/build context without a separate reviewed recovery decision. A partially enabled watcher may be stopped/disabled by the human using only the scoped `gcreation-perf-dev-deploy.path`; preserve evidence/root artifacts. Restore only the prior DEV nginx fragment using your controlled backup/config-test process. Do not remove Docker globally, alter production, purge unrelated networks/images or erase runtime data. Once a runtime exists, controlled runtime rollback/retention validation is a distinct bounded P1 evidence step through the accepted mechanism; it is not proven at this installation checkpoint.

## WHAT CODEX MUST NOT DO

No root/escalation, repository executable/module as root, Docker socket/group, systemd/Plesk/nginx administration, secret collection, WordPress filesystem writes/PHP deployment, WooCommerce configuration, live payment, customer scanning, production/main changes or frozen V4 redesign. No deployment request before installation evidence and explicit controlled-deployment approval. No P2 start while a P1 criterion/gate remains pending. No self-granted independent PASS/FROZEN and no repair cycle consumed by waiting.
