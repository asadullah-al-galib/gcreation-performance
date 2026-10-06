> CONSUMED / FAILED — HISTORICAL GATE; DO NOT RERUN. The approved request1/1 failed at non-root-build; retries0. Current action is runtime-repair-1/HUMAN_REVIEW_GATE.md; no new request or runtime action authorized. Preserve this recipe as review-time evidence only.

## PURPOSE

Obtain explicit approval for exactly ONE controlled DEV source deployment through the already installed reviewed watcher, followed by bounded read-only runtime validation. Source `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`, archive SHA `80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929`, immutable image `sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24`. P1 remains WAITING_FOR_HUMAN / execution IN_PROGRESS / full-Part independent review PENDING / repair_cycle0. Preparing this gate creates no artifact/request and performs no runtime or privileged action.

## WHY REQUIRED

The operator has supplied REAL_DEV_VERIFIED installation evidence via HUMAN_ATTESTED observations: installer exit0, exact fresh snapshot, no bytecode mutation, matched reviewed image/files/units/dependencies and active watcher. Runtime containers and deployment request are absent. This proves installation only. One constrained deployment, real health, network/sandbox/resource and rollback/retention evidence are still required for P1; root/Docker/systemd inspection belongs solely to the human. No authorization to submit a request has been granted by this recording task.

## EXACT REVIEWED ARTIFACT

- Accepted installation/deployment source: `08b395cf08523dbc5ab27f744d174b8a19bb2b4b`; never use the current evidence/governance commit as source.
- Existing verified DATA: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-08b395cf08523dbc5ab27f744d174b8a19bb2b4b.tar.gz`.
- Exact archive SHA: `80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929`.
- Observed installed root snapshot digest: `867f258b5bb1261317caa6f601becbb4c7294569ff3b5bc4903d95f926f98fc3`; independently matches the prior local expected digest. This is not a deployed runtime snapshot observation.
- Observed immutable image identity: `sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24`, matching installed runtime-image-id.
- Installation evidence: INSTALLATION_EVIDENCE.json; source repair acceptance: SECURITY_REPAIR_ACCEPTANCE.json; immutable review package: security-repair/.
- Future watcher input DATA path, only after approval: `/home/codexperf/projects/gcreation-performance/.ops/source-artifacts/08b395cf08523dbc5ab27f744d174b8a19bb2b4b.tar.gz`.

## PRECONDITIONS

- Human explicitly approves one request for this exact source/archive/image, the authorized DEV target `https://dev.gcreation.agency`, bounded read-only health/business-route refusal probes, and the scoped human runtime inspections. Confirm who will submit the ordinary-user request; Codex needs explicit permission before doing so. No root privilege is ever granted to Codex.
- Human confirms installed identity/settings still match the evidence, no running deployment/stale request/claim conflict exists, and no source/image/dependency/security policy change is required. Do not clear unexplained state, re-enable/reinstall components, replace image identities or reset valid runtime state automatically.
- Preserve the failed old stage8217aa4a13c0265efd8cb81473dd7f00c68d2c34 unchanged and the accepted fresh root snapshot immutable. Never clean/reuse/reapprove the old snapshot.
- Confirm the DEV-only health proxy is already configured under its own human approval. This gate does not authorize nginx/Plesk or WordPress/WooCommerce changes. If missing, public health stays PENDING_HUMAN until a separate narrowly scoped operator decision.
- Arrange human observation during the transient builder phase as well as after runtime start so effective build limits/isolation can be evidenced. Keep secrets/config contents out of outputs. No customer URL/browser audit, test checkout, payment or production contact is in scope.

## MINIMUM HUMAN ACTION

Approve one deployment and its designated ordinary-user submitter, observe the installed mechanism and provide one consolidated sanitized evidence set for result/health/network/image/security/resource/retention checks. This gate itself submits nothing. No retry, second deployment, restart, induced fault, manual rollback or PHP deployment is included. P1 can remain incomplete after this one deployment if required evidence is absent.

## SAFE COMMAND/UI STEPS

Future steps only, after explicit authorization. Human performs all Docker/systemd/cgroup inspections; Codex may perform only separately approved ordinary-user DATA/request/status and bounded DEV/localhost health operations.

1. Designated ordinary-user submitter verifies/export-copies the exact committed archive as bounded regular DATA into the fixed future input path and rechecks SHA `80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929`. Preserve the existing artifact exporter and accepted request trust model; never export/execute repository code as root or copy mutable workspace bytes into a release. Any existing conflicting input or unexplained trigger stops for a decision.
2. Once approved and preconditions hold, submit exactly one atomic request through the installed watcher with only this schema:

   ```json
   {"action":"deploy","commit":"08b395cf08523dbc5ab27f744d174b8a19bb2b4b","archive_sha256":"80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929"}
   ```

   The fixed trigger would be `.ops/deploy-dev.request`; it must NOT be created now. No direct controller execution, docker run, service start/restart or PHP deployment by Codex. Count the submission; maximum1, retries0. An observation timeout is not permission to submit again.
3. Observe `.ops/deploy-dev.status` for that source/archive until terminal COMPLETED or FAILED. Use the service's existing900-second ceiling and bounded polling; each agent wait <=60seconds. Persist timestamps, stage/exit information, archive/snapshot identity and any actual rollback outcome. Failure stops this attempt; never relabel FAILED/unknown as PASS or restart it automatically.
4. After reported success, confirm actual localhost `http://127.0.0.1:3101/health` and public `https://dev.gcreation.agency/perf-engine/health` GET200 with service/environment/version identity; use no authentication secret, no cookies and no request body. Do not follow redirects to another host. Bind endpoint results to the successful status/source/snapshot/image observations; generic site availability is not sufficient. Check a bounded sample of public business/admin engine paths such as `/perf-engine/admin` returns404. Record observed results; missing existing proxy setup is a separate human gate, not permission to edit nginx.
5. Human inspects only reviewed roles `gcreation-perf-dev-app`, `gcreation-perf-dev-proxy`, `gcreation-perf-dev-gateway` and transient `gcreation-perf-dev-build`. Return whitelisted identities/configuration fields, not full docker inspect or Config.Env. All use installed image `sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24` and reviewed role labels. Networks: exact64-hex persisted IDs, bridge/local, `gcreation-perf-dev-internal` Internal=true / role dev-audit and `gcreation-perf-dev-egress` Internal=false / role dev-audit-egress. App/gateway internal only; proxy alone also egress; builder network=none; no unexpected members/default bridge or Docker socket/root-host/Plesk mounts. Match observed attachments and IDs to the installed controller's checks.
6. Human captures effective UID/GID10001, cap-dropALL, no-new-privileges, reviewed seccomp, readonly roots/source/trusted mounts and bounded writable output/data/tmpfs; separate root-private mode0600 receiver-specific env files and current verified self-host deny are attested without values. App/proxy must not receive ENGINE_SECRET; gateway has no FETCH_PROXY_SECRET, proxy no APP_GATEWAY_SECRET. Image/dependency/trusted-code identities must match installation evidence. Declared flags alone do not prove effective containment.
7. Capture actual cgroup/container limits during build and runtime: shared slice4CPU/1700MiB/TasksMax256; builder3.5CPU/1500MiB replaces runtime during build; runtime app3.4CPU/1400MiB, proxy0.5CPU/150MiB, gateway0.1CPU/100MiB; PID192 per container, memory-swap cap, logs5MiB x2 per container, bounded tmpfs/output/artifacts. Include sanitized relevant cgroup values and whitelisted inspect fields/actual observations, not invented usage measurements. Identify missing transient observations explicitly rather than infer them from installed unit files.
8. Human returns observed release/failed-release counts, retained source/archive/snapshot identities and protection/cleanup outcomes, comparing the unchanged three-release bound. Inspect only; do not delete releases. Record any actual automatic rollback resulting from this single approved attempt. With no prior successful runtime, first-deployment success cannot prove rollback restoration, retention under failed attempts or live stale-request refusal. Those P1 requirements remain PENDING_HUMAN; a later explicitly approved bounded validation is required if not already evidenced. Do not submit a second request or induce failure to manufacture rollback/retention proof under this one-deployment gate.

## EXPECTED OUTPUT

One authorized terminal deployment result tied to source/archive/snapshot; successful result plus actual internal/public health200 and public business/admin404; immutable image/container/network identities; direct sanitized effective build/runtime sandbox/resource/secret-boundary observations; real retention/rollback observations or explicitly pending items. Installation snapshot evidence is retained separately from deployed snapshot evidence. COMPLETED alone does not grant D24–D27/full P1 PASS; all required criterion-level runtime/rollback evidence must be assessed first.

## SANITIZED EVIDENCE TO RETURN

Return explicit one-deployment approval/designated submitter, observation timestamps and actual commands/exit codes, terminal status, deployed source/archive/snapshot, image/container/network IDs/labels/attachments, bounded health status/body identity with redirects refused, whitelisted sandbox/mount/cgroup/resource/log fields, receiver/permission attestations without secret values, and retained-release/actual rollback results with limitations. Confirm no second request, old-stage change, production/main/WordPress/WooCommerce/nginx/Plesk mutation. Supply one consolidated non-executable evidence file under .ops/reports/P1/ or reply in chat. Never include secrets, Config.Env, full inspect, cookies, tokens, contacts or payment credentials. Mark unavailable checks PENDING_HUMAN, not PASS.

## ROLLBACK

The unchanged installed watcher may automatically attempt its accepted rollback on deployment failure if a previous runtime exists. Capture the actual stage/error/rollback result and health; do not assume restoration occurred. If this is the first runtime, absence of a prior release makes restoration unverified. Any operator restart/cleanup/manual rollback, induced failure or additional request requires a separate explicit human decision; keep bounded evidence and both root stages unchanged. No root, runtime rollback or fault action is performed by this gate preparation.

## WHAT CODEX MUST NOT DO

No request or runtime/health action now. No root/escalation/Docker socket/group/systemd/Plesk/nginx/WordPress operations, installation rerun, root snapshot/old-stage mutation, paid/live scans, secrets/customer/payment data, boundary redesign, production/main contact or P2 start. Do not treat installed image/units or this operator record as runtime containment/health/rollback PASS. Full P1 review PENDING; execution IN_PROGRESS; repair_cycle0; stop at WAITING_FOR_HUMAN.
