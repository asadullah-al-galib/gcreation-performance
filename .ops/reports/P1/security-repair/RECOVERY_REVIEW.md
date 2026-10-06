# Proposed fresh-stage recovery — review only, HOLD

No command in this procedure is authorized for execution by this candidate handoff. First obtain independent security review PASS for the exact source/archive and this recovery proposal. Then obtain a separate explicit human/operator recovery and installation decision. Codex never executes root, Docker, systemd, Plesk or nginx operations. P1 remains SECURITY_REVIEW_REQUIRED and no deployment request exists.

## Preserve and identify the failed installation

The human reported original V4 source8217aa4a13c0265efd8cb81473dd7f00c68d2c34/archive ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7: preflight PASS, installer EXIT1, generated install_preflight.cpython-36.pyc; copied root library and units exist, build-context/image absent, watcher inactive/disabled, no runtime deployment. This is HUMAN_ATTESTED, not agent-inspected.

Leave `/var/lib/gcreation-perf-review/8217aa4a13c0265efd8cb81473dd7f00c68d2c34` and its approved.json/snapshot unchanged as failure evidence. Do not delete __pycache__, amend its approved hash map, rerun its installer or use it as installation authority. Preserve `/usr/local/lib/gcreation-perf-dev`, existing reviewed unit files and root-private configuration; no cleanup/recovery is performed now.

Before any approved recovery, the human inventories only scoped root-owned ownership/modes/hashes and watcher state without printing environment/configuration values. Compare copied deploy_controller.py, deploy-dev.sh, runtime.Dockerfile, seccomp_profile.json, install_preflight.py and the three gcreation-perf-dev units against their verified archived bytes. They are unchanged in the candidate; same-byte copies may remain. Confirm build-context, installed image seal/dependency-baseline outputs and runtime image are absent, watcher inactive/disabled, no existing runtime and no stale request including dangling links. Unexpected contents, identities, active units, partial build-context or runtime evidence require a new human recovery decision; do not automatically delete, overwrite, rename or disable anything.

## Separately approved new root stage

- Proposed source: `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`.
- Proposed DATA archive: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-08b395cf08523dbc5ab27f744d174b8a19bb2b4b.tar.gz`.
- Proposed archive SHA-256: `80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929`.
- New root staging path: `/var/lib/gcreation-perf-review/08b395cf08523dbc5ab27f744d174b8a19bb2b4b`; it must not already exist.
- Locally expected snapshot digest: `867f258b5bb1261317caa6f601becbb4c7294569ff3b5bc4903d95f926f98fc3`; this is not installed evidence.

The future human uses the existing reviewed ROOT_TRUST_TRANSITION.md system-only bootstrap with this new commit and independently approved hash. The recipe is byte-identical to V4. Copy archive as DATA into fresh root-only staging, check the root-owned copy against the separately approved SHA, safely extract regular members, bind approved.json, and verify exact root ownership and file hashes. Manually supply the reviewed system-only stdin; do not execute/source a repository document, pipe repository text into root Python or execute any repository module as root. Preserve env -i/fixed PATH/Python -I. No in-place extraction over the old snapshot and no relaxation of verify_snapshot.

Retain/check root-private runtime.env mode0600 and distinct secret receivers/verified current DEV self-host deny without echoing its contents. Verify existing protected ancestors/installed library are root-owned, symlink-free and non-writable by codexperf. Existing like-for-like library/unit copies can be retained for the separately approved installer to copy again; this deliberately avoids blanket deletion. If source bytes differ from the verified review set, stop for a human decision.

Only after security PASS, explicit human recovery approval, fresh verified snapshot and all unchanged preconditions, the human installer invocation would be:

```sh
/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /bin/bash /var/lib/gcreation-perf-review/08b395cf08523dbc5ab27f744d174b8a19bb2b4b/snapshot/ops/dev/install-root.sh 80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929 08b395cf08523dbc5ab27f744d174b8a19bb2b4b
```

This is a future review recipe, not permission to run now. Its prepare and seal child starts use -I -B. Installer preflight, archive identity, ownership checks, immutable image preparation, network/resource/security configuration and final stale-trigger recheck remain unchanged. Existing copied root files/units may be overwritten only by the same verified candidate bytes during that separately approved human installation; the failed root snapshot is never modified. Do not issue a deployment request or perform WordPress/nginx/Plesk/configuration changes as part of reviewing this repair.

## Evidence and stop conditions

Human returns sanitized exact source/archive/root snapshot hash/ownership confirmation, installer actual exit/stage, absence of import-generated files before/after prepare and seal, installed immutable image/dependency identity and watcher state. Never return secrets, full inspect/env output, cookies, tokens or customer/payment data. Any hash/preflight/ownership/build failure stops recovery; retain evidence and do not consume another repair silently or clean generated snapshot files to force a PASS.

This candidate review does not accept installation, effective Docker/cgroups, offline runtime deployment, health, rollback/retention or P1 completion. Those remain separately gated evidence. P2 stays NOT_STARTED; production/main and unrelated DEV/WordPress/WooCommerce paths stay untouched. No rollout, retry, cleanup or recovery has been performed by Codex.
