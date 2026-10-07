# P1 gateway-only Stage 3 cause-attribution analysis

**HARD_BLOCKED / P1 BLOCKED.** Analysis and evidence recording only. No agent Docker, controller, gateway/app/proxy, HTTP, systemctl, privileged, protected-path inspection or secret/raw gateway-log read occurred.

## Verified handoff and conclusions

Stage 3 handoff VERIFIED SHA256 8660233e467c3b77e5beeff66d0125109c4eb78221f1ef4bd571420e1f916ba0 / 1,167 bytes. Human gateway-only execution count=1, complete=true; no further gateway/runtime execution authority. Operator reports RUNNING, ExitCode=0, restart count=0, OOM=NO, state error=NO, NO_LOG_OUTPUT; lifecycle PASS_OBSERVED at the reported observation only. PORT_3101_EXACT_PUBLISH=NO; INTERNAL_NETWORK_EXACT=YES; localhost URL_ERROR:CONNECTION_REFUSED; host-to-gateway transport FAIL_OBSERVED. Cause attribution GATEWAY_RUNNING_BUT_LOCALHOST_TRANSPORT_UNREACHABLE; underlying root cause/component NOT_ESTABLISHED; no control-flow contradiction. Stage2 localhost failure reproduced PARTIALLY (URL_ERROR class, not exact historical cause/full-runtime conditions). Actual 3101/tcp mapping, comparison criteria and observation/probe timing are unreported. Reviewed controller expects 127.0.0.1:3101:3101; a running container alone does not prove a bound listener. Controller/image/network identity attestations match committed reviewed/prior identities; no new host verification. P1 BLOCKED / HARD_BLOCKED, full review PENDING; repair_cycle=2, failed repair cycles=2, REPAIR_2 failed/consumed1/1, all official attempts consumed, automatic retries=0, budget exhausted. P2–P7 NOT_STARTED; P0 FROZEN/human PASS; production/main untouched. HUMAN DECISION REQUIRED. The gateway-only handoff reports PORT_3101_EXACT_PUBLISH=NO and URL_ERROR:CONNECTION_REFUSED, but omits the actual 3101/tcp publication and the exact comparison criteria. Decide whether to authorize narrowly scoped evidence sufficient to explain that mismatch and relate it to Stage2. No additional read, probe, gateway/full-runtime execution, repair, deployment or budget extension is authorized.

| Classification                      | Result                                              |
| ----------------------------------- | --------------------------------------------------- |
| STAGE3 HANDOFF                      | VERIFIED                                            |
| GATEWAY DOCKER RUN                  | CREATED                                             |
| GATEWAY STATE                       | RUNNING                                             |
| GATEWAY EXIT CODE                   | 0                                                   |
| GATEWAY RESTART COUNT               | 0                                                   |
| GATEWAY OOM                         | NO                                                  |
| PORT 3101 EXACT PUBLISH             | NO                                                  |
| INTERNAL NETWORK EXACT              | YES                                                 |
| LOCALHOST HEALTH PROBE              | URL_ERROR:CONNECTION_REFUSED                        |
| GATEWAY LOG CLASSIFICATION          | NO_LOG_OUTPUT                                       |
| HOST TO GATEWAY TRANSPORT           | FAIL_OBSERVED                                       |
| GATEWAY PROCESS LIFECYCLE           | PASS_OBSERVED                                       |
| STAGE2 LOCALHOST FAILURE REPRODUCED | PARTIALLY                                           |
| CAUSE ATTRIBUTION CLASS             | GATEWAY_RUNNING_BUT_LOCALHOST_TRANSPORT_UNREACHABLE |
| UNDERLYING ROOT CAUSE               | NOT_ESTABLISHED                                     |
| UNDERLYING COMPONENT                | NOT_ESTABLISHED                                     |
| CONTROL FLOW CONTRADICTION          | NO                                                  |
| PORT PUBLICATION MISMATCH REPORTED  | YES                                                 |
| GATEWAY ONLY TRANSPORT              | FAIL_OBSERVED                                       |
| STAGE2 FAILURE DOMAIN               | NOT_ESTABLISHED                                     |

The exact-publication check failed: reviewed controller expects `127.0.0.1:3101:3101`, but the handoff says `PORT_3101_EXACT_PUBLISH=NO`. Actual `3101/tcp` bindings/effective publication and the check expression/compared values are **not supplied**. This establishes a reported mismatch, not its mechanism. Do not infer omitted `-p`, a Docker bug, a firewall fault, an internal-network prohibition or a launcher defect. Case F applies; Case C's exact-publication=YES prerequisite is absent.

Reported running state, restart count0, exit code0, OOM=NO and state-error=NO support **PASS_OBSERVED lifecycle at that observation**. They do not prove a listening socket or continuous readiness. Exit code0 while running is not proof of a completed successful exit. `GATEWAY_FINISHED_AT=0001-01-01T00:00:00Z` is retained as a sentinel; it is not a real shutdown date. `NO_LOG_OUTPUT` establishes no specific error or successful initialization. Start time is `2026-10-07T09:30:45.664936327Z`; state, port-check and probe timestamps/relative order are absent, so no startup-race diagnosis is established or excluded.

`URL_ERROR:CONNECTION_REFUSED` supports **FAIL_OBSERVED host-to-gateway transport** in this diagnostic. A running process plus this refusal and the reported mismatch does not uniquely identify the failing host publication, listener, runtime or network component. Underlying cause and component remain **NOT_ESTABLISHED**. No HTTP response was supplied, so transport reachability is not proven.

## Exact committed source semantics and identities

- Controller candidate `b060ff430854046df7490875ac402d9df909b43a`, committed HEAD and repository controller bytes all equal SHA256 `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f`; the reported installed hash matches. Host installation remains human attestation.
- Accepted gateway source commit `0ac34ba50ab3192abfe2ae425c4283879484258e`, controller candidate, committed HEAD and workspace gateway bytes agree, SHA256 `d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c`.
- Reviewed controller launches `node /opt/gcreation-trusted/ops/dev/trusted/gateway.mjs`, publishes `127.0.0.1:3101:3101`, and requires localhost health before DEV homepage health. Inspection was Git text/controller AST only; no repository runtime was executed.
- Gateway source binds `server.listen(3101, "0.0.0.0")`. `/health` skips client authentication but is still forwarded to the fixed `http://gcreation-perf-dev-app:3101/` upstream. An upstream connection error emits502 if the gateway is reachable. With the app intentionally absent,502 would prove host-to-gateway/listener reachability; **no502 or other HTTP response was observed here**. No HTTP200 contradiction is demonstrated.
- Operator-reported image `sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a` matches reviewed/Stage2 identity. Internal network ID `e94996e300b479ee92c339e460cd408edd48995093f4d5089db44e69515719f3` matches the committed post-failure inventory. Exact internal-network check is attested YES; no full membership/port metadata or fresh host inspection is supplied.

## Stage 2 correlation and attribution limits

Stage2 remains unchanged: HEALTH_FAILED,30/30 localhost URL_ERROR, no retained HTTP status, homepage NOT_REACHED. Its failed diagnostic predicate LOCALHOST_ENGINE_HEALTH remains PROVEN_IN_DIAGNOSTIC_EXECUTION; underlying cause/component remain unknown. Stage3 reproduces **the URL_ERROR transport class only**, now reporting CONNECTION_REFUSED with app/proxy intentionally absent. Therefore reproduction is **PARTIALLY**, not proof of the same exact full-runtime defect. Stage2 had no retained errno/message; its historical URL_ERROR cannot be relabeled CONNECTION_REFUSED. Gateway-only isolation and a reported publication mismatch do not establish full-runtime equivalence.

Gateway-only transport did not pass, so `FULL_RUNTIME_SPECIFIC_OR_TRANSIENT` is **not established**. Stage2 is not invalidated. Original official REPAIR_2 terminal status/runtime-health deadline failure remains untouched; no new historical inner-predicate attribution or P1 runtime acceptance follows.

## Every supplied field and unreported evidence

All 32 fields are retained exactly, with typed boolean/integer counterparts in ANALYSIS.json. Missing/unreported values are null, never synthesized.

| Field                              | Exact supplied value                                                      |
| ---------------------------------- | ------------------------------------------------------------------------- |
| RESULT                             | `COMPLETE`                                                                |
| INSTALLED_CONTROLLER_SHA256        | `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f`        |
| RUNTIME_IMAGE_ID                   | `sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a` |
| INTERNAL_NETWORK_ID                | `e94996e300b479ee92c339e460cd408edd48995093f4d5089db44e69515719f3`        |
| HOST_3101_LISTENER_BEFORE          | `NO`                                                                      |
| GATEWAY_DOCKER_RUN_CREATED         | `YES`                                                                     |
| GATEWAY_STATE_STATUS               | `running`                                                                 |
| GATEWAY_RUNNING                    | `YES`                                                                     |
| GATEWAY_RESTARTING                 | `NO`                                                                      |
| GATEWAY_EXIT_CODE                  | `0`                                                                       |
| GATEWAY_OOM_KILLED                 | `NO`                                                                      |
| GATEWAY_RESTART_COUNT              | `0`                                                                       |
| GATEWAY_STATE_ERROR_PRESENT        | `NO`                                                                      |
| GATEWAY_STARTED_AT                 | `2026-10-07T09:30:45.664936327Z`                                          |
| GATEWAY_FINISHED_AT                | `0001-01-01T00:00:00Z`                                                    |
| PORT_3101_EXACT_PUBLISH            | `NO`                                                                      |
| INTERNAL_NETWORK_EXACT             | `YES`                                                                     |
| LOCALHOST_HEALTH_PROBE             | `URL_ERROR:CONNECTION_REFUSED`                                            |
| GATEWAY_LOG_CLASSIFICATION         | `NO_LOG_OUTPUT`                                                           |
| CAUSE_ATTRIBUTION_CLASS            | `GATEWAY_RUNNING_BUT_LOCALHOST_TRANSPORT_UNREACHABLE`                     |
| FULL_RUNTIME_EXECUTION             | `NO`                                                                      |
| APP_CONTAINER_STARTED              | `NO`                                                                      |
| PROXY_CONTAINER_STARTED            | `NO`                                                                      |
| DEPLOY_PATH_USED                   | `NO`                                                                      |
| DEPLOYMENT_REQUEST                 | `NO`                                                                      |
| REPAIR_COUNTER_CHANGE              | `NO`                                                                      |
| REPAIR_3_AUTHORIZED                | `NO`                                                                      |
| REPAIR_BUDGET_RESET                | `NO`                                                                      |
| P2_STARTED                         | `NO`                                                                      |
| PRODUCTION_MAIN_TOUCHED            | `NO`                                                                      |
| DIAGNOSTIC_GATEWAY_CONTAINER_AFTER | `ABSENT`                                                                  |
| STAGE3_CLEANUP_RESULT              | `PASS`                                                                    |

The human request separately reports ONE_COMPLETED. Stage3 authorized=true, execution_count=1 and complete=true describe **that past human action only**. Further gateway execution authorized=false. Cleanup PASS / diagnostic gateway ABSENT are operator attestations about that isolated diagnostic resource; no agent cleanup or inference about the full official resource inventory is made.

The primary missing criterion is the actual sanitized `3101/tcp` host-publication result and exact comparison definition/values behind `PORT_3101_EXACT_PUBLISH=NO`. The container ID/exact historical diagnostic command, post-start socket readiness, probe/state/port observation times and Stage2 exact errno are also unreported. No specific correction can be selected from these summaries. Source/controller/gateway-image/network/runtime-config change requirements and a future repair's security impact remain UNKNOWN.

## Human decision and preserved governance

HUMAN DECISION REQUIRED. The gateway-only handoff reports PORT_3101_EXACT_PUBLISH=NO and URL_ERROR:CONNECTION_REFUSED, but omits the actual 3101/tcp publication and the exact comparison criteria. Decide whether to authorize narrowly scoped evidence sufficient to explain that mismatch and relate it to Stage2. No additional read, probe, gateway/full-runtime execution, repair, deployment or budget extension is authorized.

No concrete root cause is proven and no exception repair is implemented. INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1; repair_cycle2; failed repair cycles2; automatic retries0; exhausted budget. No REPAIR_3, budget extension/reset, deployment request or next Part is created. V4 code/enforcement boundaries remain unchanged. P1 remains BLOCKED/full independent review PENDING; P2–P7 NOT_STARTED; P0 FROZEN/human PASS; production/main untouched.

## Documentation verification and changed files

22 offline evidence/identity/source checks PASS. Verification reads supplied handoff and committed source as text/AST; no application/runtime tests or live measurements are claimed. Byte-identical retained handoff, parsed fields, documentation/checksum consistency, prior evidence preservation and Git whitespace are checked before commit. New event0020 is append-only and equals LATEST_CHECKPOINT.json.

- `.ops/ACTION_REQUIRED.md`
- `.ops/ORCHESTRATOR_STATUS.json`
- `.ops/PROJECT_STATE.md`
- `.ops/PROJECT_STATUS.md`
- `.ops/oversight/LATEST_CHECKPOINT.json`
- `.ops/oversight/LATEST_CHECKPOINT.md`
- `.ops/oversight/events/0020-P1-gateway-only-stage3-analysis.json`
- `.ops/reports/P1/CHECKSUMS.sha256`
- `.ops/reports/P1/EVIDENCE.json`
- `.ops/reports/P1/REPORT.md`
- `.ops/reports/P1/gateway-only-stage3/ANALYSIS.json`
- `.ops/reports/P1/gateway-only-stage3/CHECKSUMS.sha256`
- `.ops/reports/P1/gateway-only-stage3/HANDOFF.txt`
- `.ops/reports/P1/gateway-only-stage3/REPORT.md`

Prior Stage1/Stage2 packages, previous events, original failures and reviewed source/tests/dependencies/privileged kit/product documents remain unchanged. Develop alone is committed/pushed; main read-only identity remains `c724ac3b50bc44d71f8620bb4ac0cccfae890de2`.

**NO REPAIR OR DEPLOYMENT IS AUTHORIZED. No further gateway or full-runtime execution is authorized.**
