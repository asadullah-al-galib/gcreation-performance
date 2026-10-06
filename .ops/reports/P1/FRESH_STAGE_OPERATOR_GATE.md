## PURPOSE

Obtain separate human/operator approval and perform minimum fresh-stage recovery for the independently accepted repair source `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`. P1 is WAITING_FOR_HUMAN; execution IN_PROGRESS, full-Part independent review PENDING, repair_cycle0. No recovery or installation is authorized by recording the source review PASS.

## WHY REQUIRED

The human granted independent security PASS for the two -I -B source changes only. Root staging, existing copied-file verification, image/systemd installation and any recovery are operator actions. Codex has no privilege. The prior real-host failure/partial state is human-attested in security-repair/HOST_FAILURE.json; it has not been inspected or changed by Codex.

## EXACT REVIEWED ARTIFACT

- Independently accepted source: `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`; acceptance record: SECURITY_REPAIR_ACCEPTANCE.json.
- Exact DATA archive: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-08b395cf08523dbc5ab27f744d174b8a19bb2b4b.tar.gz`.
- Proposed archive SHA-256 supplied by the human: `80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929`. Verify and separately approve this identity for root staging; source PASS alone does not grant installation.
- Archive source manifest: security-repair/SOURCE_MANIFEST.sha256; file SHA `11b0c7507058a4fbd56e12398b96547ed7d2b9724153d05ecd44e747460a28d7` (105 members).
- Expected candidate snapshot digest: `867f258b5bb1261317caa6f601becbb4c7294569ff3b5bc4903d95f926f98fc3`; locally calculated, not observed root/runtime evidence.
- Unchanged bootstrap recipe: `/home/codexperf/projects/gcreation-performance/ops/dev/ROOT_TRUST_TRANSITION.md`, also in this archive. The current approval-state commit is metadata, not a replacement installation source.

## PRECONDITIONS

- Obtain explicit human/operator approval of this scoped fresh-stage recovery and exact archive/hash before any root action. Do not infer that approval from the source PASS or this gate file.
- Preserve `/var/lib/gcreation-perf-review/8217aa4a13c0265efd8cb81473dd7f00c68d2c34` and its contaminated snapshot/approved.json unchanged. Never reuse, clean, rehash to accept bytecode, or rerun that old installer.
- New root stage `/var/lib/gcreation-perf-review/08b395cf08523dbc5ab27f744d174b8a19bb2b4b` must not exist; protected ancestors and installed inputs must remain root-owned, symlink-free and non-writable by codexperf. No deployment request, including dangling symlink, may exist.
- Human verifies reported partial state: reviewed files/units copied; build-context and runtime image absent; watcher inactive/disabled; no runtime deployment. Check installed image seal/dependency-baseline outputs and runtime state without assuming absence from old reporting. Any unexpected state or hash mismatch stops for a new human decision; no automatic cleanup.
- Human verifies unchanged Docker/systemd/BuildKit/x86_64 prerequisites and existing root-private runtime.env0600, secret distinction/placement and current DEV self-host deny without returning values. Missing prerequisites do not authorize host/security redesign.

## MINIMUM HUMAN ACTION

Separately approve the recovery, verify copied partial-install files against the candidate's unchanged bytes, create a new root-only stage from exact hash-verified DATA using the unchanged system-only bootstrap, then execute the accepted installer solely from that fresh verified root-owned snapshot. Preserve the failed stage and existing like-for-like copied files/units. No deployment request, runtime acceptance, nginx/Plesk, WordPress/WooCommerce or production change is included in this gate.

## SAFE COMMAND/UI STEPS

Human-only, conditional on explicit recovery approval; Codex executes none. A single install command cannot safely replace fresh staging, private configuration and partial-state verification.

1. Verify archive DATA using the system utility:

   ```sh
   /usr/bin/sha256sum /home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-08b395cf08523dbc5ab27f744d174b8a19bb2b4b.tar.gz
   ```

   Require the exact proposed SHA above and independently approve that value for staging. Check candidate manifest/committed source identity. Do not derive root approval automatically from developer-writable metadata.
2. Human compares the previously copied deploy_controller.py, deploy-dev.sh, runtime.Dockerfile, seccomp_profile.json, install_preflight.py and three gcreation-perf-dev unit files to corresponding verified candidate archive bytes. These inputs did not change. Leave matching root-owned files/units in place; the approved installer may recopy the same bytes. Unexpected contents or active/build/runtime state require a separate recovery decision. Do not delete directories, images, caches, units or secrets as a shortcut.
3. Manually use the unchanged ROOT_TRUST_TRANSITION.md system-only bootstrap with `COMMIT='08b395cf08523dbc5ab27f744d174b8a19bb2b4b'` and, only after approving the verified hash, `APPROVED_SHA='80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929'`. It copies archive as DATA into a fresh root-only stage, rechecks the root-owned copy, validates/extracts regular safe members, creates approved.json and verifies ownership/hashes. Preserve env -i, fixed PATH, Python -I and all fail-closed checks. Do not source/execute a repository document, generate root stdin from repository bytes, or execute a repository module as root. Do not extract over the old stage.
4. Only after all preconditions and fresh snapshot checks, the separately approved human installer command is:

   ```sh
   /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /bin/bash /var/lib/gcreation-perf-review/08b395cf08523dbc5ab27f744d174b8a19bb2b4b/snapshot/ops/dev/install-root.sh 80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929 08b395cf08523dbc5ab27f744d174b8a19bb2b4b
   ```

   This is a future operator step, not authorization to run now. It retains verify_snapshot and uses -I -B for prepare/seal. Expected image/systemd operations are solely the unchanged reviewed installer behavior. Existing matching copied files/units may be recopied by that approved installer; the failed snapshot remains untouched. Stop on any nonzero exit or unexpected state.
5. Human verifies exact new snapshot content/ownership before and after image setup, no import-generated .pyc or __pycache__, installed component hashes, immutable image ID and dependency hashes, installer exit0 and watcher state. Return only sanitized evidence; never print environment contents, full Docker inspect or private credential configuration. No deployment request is created at this step.

## EXPECTED OUTPUT

Explicit operator approval; exact archive/root-copy SHA and source identity match; fresh root-owned105-member snapshot verifies without bytecode mutation; installer exits0; installed immutable image/dependency identities and reviewed root-owned files match; watcher state reported with no stale trigger. Old failed stage remains unchanged. These observations establish installation evidence only, not D24–D27 runtime PASS or full P1 acceptance.

## SANITIZED EVIDENCE TO RETURN

Return actual timestamp, approval decision, source/archive/root-stage identity, pre/post snapshot hash/ownership checks, installer stage/exit code, absence of generated bytecode, installed file/image/dependency hashes and watcher state. Confirm old stage preservation and no deployment request/runtime deployment or production/main/WordPress/WooCommerce/nginx/Plesk change. Attest private configuration permissions/secret separation/deny checks without returning values or secret hashes. If already recovered or state differs, report scoped evidence instead of rerunning. Reply in chat or supply sanitized non-executable evidence under .ops/reports/P1/. A marker alone never proves installation or runtime acceptance. Subsequent controlled deployment/runtime validation requires its separate authorization; none is requested by this gate.

## ROLLBACK

On unexpected partial state or failed staging/preflight/build/install, stop and retain exact sanitized stage/error/exit evidence. Do not reuse/clean either snapshot, delete build-context, amend approved.json or purge installed files/images/networks. Any cleanup or operator rollback beyond the explicitly approved recovery requires a separate human decision. Preserve the old failed stage and private settings. No runtime rollback is inferred because no runtime deployment has been reported.

## WHAT CODEX MUST NOT DO

No root/escalation, Docker socket/group, systemd/Plesk/nginx administration, existing stage/partial-install mutation, bytecode cleanup/verifier bypass, secret collection, repository executable as root, deployment request, runtime continuation, WordPress/WooCommerce change, production/main action or P2 start. Candidate source security PASS is not full P1 independent PASS/FROZEN. Stop at WAITING_FOR_HUMAN; repair_cycle remains0.
