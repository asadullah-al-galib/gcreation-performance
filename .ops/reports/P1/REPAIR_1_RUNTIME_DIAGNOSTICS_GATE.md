# P1 REPAIR_1 runtime failure — read-only operator diagnostics

STATE: HUMAN_CAPABILITY_GATE. Classification RELIABILITY_CRITICAL; business mapping RELIABILITY / SECURITY / MVP_RELEASE. REPAIR_1 request1/1 was submitted and consumed, retry0, candidate134ddfbe/archive d2c69e1a.... Terminal installed watcher status: FAILED / runtime-health / RuntimeError / rollback=false. Controller refresh remains PASS. P1 incomplete; root cause NOT_ESTABLISHED; REPAIR_2 has not been implemented or attempted. This is an evidence/capability request, not repeat approval or a retry gate.

The agent cannot access protected runtime/service/container diagnostics through an approved constrained interface. Smallest human action: return one bounded sanitized read-only diagnostic bundle for this single attempt. Preserve all existing state; do not rerun/restart/reset services, deploy, rebuild, refresh, clean, modify configuration or execute repository modules. No production/main/WordPress/Plesk/nginx work.

Return observation times and actual scoped command/check exit codes. Inspect only the fixed gCreation DEV units, image and container names below. Do not return full inspect, Config.Env, argv/secret values, tokens, cookies, payment credentials, private configuration contents/hashes or unrelated host/customer logs.

1. Terminal deployment status (already available to Codex) and fixed deploy service properties: ActiveState, SubState, Result, ExecMainCode, ExecMainStatus, ExecMainStartTimestamp, ExecMainExitTimestamp. Read-only example for the designated operator:

   ```sh
   /usr/bin/systemctl show gcreation-perf-dev-deploy.service --property=ActiveState,SubState,Result,ExecMainCode,ExecMainStatus,ExecMainStartTimestamp,ExecMainExitTimestamp
   ```

2. At most the last80 lines of this DEV deploy service's journal for this attempt, bounded to the actual submission/terminal-observation time range recorded in REPAIR_1_DEPLOYMENT_ATTEMPT.json. Keep the raw journal root-private; return only reviewed/redacted failure traceback lines and command exit/stage evidence. A traceback line can identify which reviewed start_runtime operation failed even though stdout/stderr is deliberately suppressed. Do not infer a missing error message or fabricate subprocess output.

3. Read-only exact-name container inventory for gcreation-perf-dev-build, gcreation-perf-dev-app, gcreation-perf-dev-proxy and gcreation-perf-dev-gateway. Return only existing/absent, ID, role label, image ID, state and exit code. If a fixed container survives, return at most40 redacted log lines relevant to startup plus the exact failed scoped operation from the service traceback. Missing/removed containers or logs are unavailable evidence, not permission to recreate or run them. Example whitelisted inspect template, only for an existing fixed-name container:

   ```sh
   /usr/bin/docker inspect --format '{{json .Id}} {{json .Image}} {{json .State.Status}} {{json .State.ExitCode}} {{json .Config.Labels}}' gcreation-perf-dev-proxy
   ```

4. Installed runtime-image-id equality against immutable image sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24. Inspect this exact image read-only for Id, Config.User and Config.WorkingDir only; no build/tag/pull or env output. Return any concrete rejection from Docker/service/runtime that explains the failed start. Do not change anything in response.

5. Attest request/claim absent, failed release and old stages/evidence preserved, no additional deployment/retry/refresh/installer/image/configuration action occurred. If a timestamp or check is unavailable, say so.

No CPU/RAM/PID usage, network identity, health, retention success, rollback restoration or root cause is claimed from static flags. No full runtime acceptance is possible from the failed status. If this bundle establishes a concrete defect, Codex can assess the smallest relevant REPAIR_2 change under P0.2; a frozen V4 trust/security boundary change stops at SECURITY_REVIEW_REQUIRED before implementation. If the available logs cannot establish the cause, identify that gap; never retry unchanged source for diagnosis.
