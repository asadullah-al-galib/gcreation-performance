# P1 gateway Stage 3B port-binding and listener attribution

**HARD_BLOCKED / P1 BLOCKED.** Analysis and evidence recording only. Codex ran no Docker, controller, gateway/app/proxy, HTTP probe, systemctl or privileged action, and read no protected path, secret or raw gateway log.

## Verified handoff and classification

Stage3B handoff VERIFIED SHA256 25b1a14c0cfc93c425ffbf65d4d926e54fac8e653b108f799bd523766a2aee4a / 1,364 bytes. One completed human gateway-only execution; authorized=true, execution_count=1, complete=true for that past action only; further gateway execution authorized=false. Operator reports running gateway and container listener STATE=LISTEN;TOTAL=1;IPV4=1;IPV6=0. HostConfig 3101/tcp present, one IPV4_LOOPBACK_EXACT binding, host port3101, exact=YES, other port keys=NO. NetworkSettings 3101/tcp absent, zero bindings, exact=NO, other port keys=NO. Requested port config CORRECT; effective publication MISMATCH; container listener PASS_OBSERVED; localhost URL_ERROR:CONNECTION_REFUSED, host-to-gateway transport FAIL_OBSERVED. Root cause class PROVEN_COMPONENT_CLASS; component DOCKER_PORT_PUBLICATION_LAYER in this isolated observation; exact underlying root cause NOT_ESTABLISHED. Host LISTEN totals0 before/after are supporting evidence only, not standalone failure proof. Stage3 port mismatch reproduced YES at reported-check level; previous checker/metadata/mechanism remain unproven. Stage2 localhost failure reproduced PARTIALLY (URL_ERROR class); historical exact cause unchanged. No control-flow contradiction. Runtime/install/image/network/listener/cleanup facts remain human attestation. P1 BLOCKED / HARD_BLOCKED, full review PENDING; repair_cycle=2, failed repair cycles=2, INITIAL/REPAIR_1/REPAIR_2 failed/consumed, REPAIR_2 attempts1/1, retries0, exhausted budget. P0 FROZEN/human PASS; P2–P7 NOT_STARTED; production/main untouched. PROPOSED_EXCEPTION_REPAIR — NOT AUTHORIZED. Human decision required on the observed requested/effective Docker port-publication mismatch. Exact daemon/network mechanism and intervention remain unknown. Any further evidence collection, gateway/full-runtime execution, repair or deployment requires NEW explicit human authority; no REPAIR_3 or repair-budget extension/reset is authorized.

| Classification                      | Result                                                         |
| ----------------------------------- | -------------------------------------------------------------- |
| STAGE3B HANDOFF                     | VERIFIED                                                       |
| GATEWAY RUNNING                     | YES                                                            |
| HOSTCONFIG 3101 PRESENT             | YES                                                            |
| HOSTCONFIG BINDING COUNT            | 1                                                              |
| HOSTCONFIG EXACT LOOPBACK 3101      | YES                                                            |
| HOSTCONFIG SANITIZED BINDING        | IP_CLASS=IPV4_LOOPBACK_EXACT;HOST_PORT=3101                    |
| NETWORKSETTINGS 3101 PRESENT        | NO                                                             |
| NETWORKSETTINGS BINDING COUNT       | 0                                                              |
| NETWORKSETTINGS EXACT LOOPBACK 3101 | NO                                                             |
| NETWORKSETTINGS SANITIZED BINDING   | ABSENT;BINDING_COUNT=0                                         |
| CONTAINER 3101 LISTENER             | STATE=LISTEN;TOTAL=1;IPV4=1;IPV6=0                             |
| HOST LISTENER BEFORE                | EXACT_LOOPBACK=0;ANY_IPV4=0;IPV6_LOOPBACK=0;ANY_IPV6=0;TOTAL=0 |
| HOST LISTENER AFTER                 | EXACT_LOOPBACK=0;ANY_IPV4=0;IPV6_LOOPBACK=0;ANY_IPV6=0;TOTAL=0 |
| LOCALHOST HEALTH PROBE              | URL_ERROR:CONNECTION_REFUSED                                   |
| DOCKER REQUESTED PORT CONFIG        | CORRECT                                                        |
| DOCKER EFFECTIVE PORT PUBLICATION   | MISMATCH                                                       |
| CONTAINER GATEWAY LISTENER          | PASS_OBSERVED                                                  |
| HOST TO GATEWAY TRANSPORT           | FAIL_OBSERVED                                                  |
| STAGE3 PORT MISMATCH REPRODUCED     | YES                                                            |
| STAGE2 LOCALHOST FAILURE REPRODUCED | PARTIALLY                                                      |
| ROOT CAUSE CLASS                    | PROVEN_COMPONENT_CLASS                                         |
| UNDERLYING ROOT CAUSE               | NOT_ESTABLISHED                                                |
| UNDERLYING COMPONENT                | DOCKER_PORT_PUBLICATION_LAYER                                  |
| CONTROL FLOW CONTRADICTION          | NO                                                             |

Case C applies: the operator-retained HostConfig requested binding matches the reviewed loopback mapping, while NetworkSettings reports no effective `3101/tcp` binding. The container TCP/3101 listener is present, and the host HTTP probe reports connection refusal. These combined observations support **PROVEN_COMPONENT_CLASS / DOCKER_PORT_PUBLICATION_LAYER** in this isolated execution. The exact Docker daemon/network/publication mechanism remains **NOT_ESTABLISHED**.

This is not a requested HostIp/HostPort mismatch or multiple-binding case: HostConfig has exactly one `IPV4_LOOPBACK_EXACT` binding with HostPort3101 and no other port keys. NetworkSettings reports `3101/tcp` absent, count0, exact=NO and no other port keys; it supplies no binding rows. The retained safe classes/flags are operator evidence, not raw Docker JSON independently inspected by Codex.

Container listener `STATE=LISTEN;TOTAL=1;IPV4=1;IPV6=0` supports PASS_OBSERVED. Socket-owner/PID and exact container-side bind address are absent; successful credential/import/entrypoint details are not inferred. Gateway running at observation is attested YES, but Stage3B provides no restart/exit/OOM metadata or observation/probe timestamps; Stage3 values are not copied into this execution.

Host listener totals0 before/after are **supporting evidence only**. Per the supplied analysis rule, Docker NAT publication can operate without a host userspace LISTEN socket. No contradiction or daemon/firewall/iptables/docker-proxy cause is inferred from host `/proc` absence. Classification instead uses requested/effective Docker mapping, container listener and the failed probe together.

## Exact committed source and identities

- Reviewed controller candidate `b060ff430854046df7490875ac402d9df909b43a`, committed HEAD and workspace bytes equal SHA256 `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f`, matching the installed-hash attestation.
- Gateway accepted source `0ac34ba50ab3192abfe2ae425c4283879484258e`, reviewed candidate, committed HEAD and workspace bytes match SHA256 `d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c`.
- Controller requests `-p 127.0.0.1:3101:3101` and launches `node /opt/gcreation-trusted/ops/dev/trusted/gateway.mjs`. Expected requested/effective Docker key is `3101/tcp`, exactly one binding, HostIp127.0.0.1 and HostPort3101. The diagnostic HostConfig matches this source request; **the official controller was not executed**, so this does not prove it submitted the diagnostic command.
- Gateway source binds `server.listen(3101, "0.0.0.0")`. Authentication-exempt `/health` still forwards to `http://gcreation-perf-dev-app:3101/`. HTTP502 would be compatible with absent app and reachable gateway; no HTTP response was supplied here, so that success case was not observed. No HTTP200 contradiction is demonstrated.
- Operator image `sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a` and internal network ID `e94996e300b479ee92c339e460cd408edd48995093f4d5089db44e69515719f3` match the previously reviewed/retained identities. Stage3B does not supply a complete network membership map.

Git text/controller AST inspection only; no source module/runtime was executed or protected installed state inspected.

## Stage 3 and Stage 2 correlation

**Stage3 port mismatch reproduced: YES at reported-check level.** Stage3B requested HostConfig is correct, and its effective NetworkSettings binding is absent. This is a retained explanation of the current exact-publication failure and is compatible with Stage3's `PORT_3101_EXACT_PUBLISH=NO` / CONNECTION_REFUSED. Stage3's actual metadata/check definition were not supplied, so Stage3B does not prove what the earlier check compared or that the earlier mechanism was identical. Stage3 is a distinct completed execution; its package, flags and uncertainty remain unchanged.

**Stage2 localhost failure reproduced: PARTIALLY.** The URL_ERROR class recurs, now with CONNECTION_REFUSED in gateway-only mode. Stage2's30 LOCALHOST_ENGINE_HEALTH URL_ERROR / HTTP status NONE and homepage NOT_REACHED observations remain unchanged. Its errno/effective mapping were unreported, so exact full-runtime/historical cause attribution remains unproven. Original official REPAIR_2 terminal status and runtime-health deadline evidence remain immutable. This component finding grants no P1 runtime acceptance.

## Every supplied field and missing information

All 32 fields, including every supplied binding field, are retained exactly and typed in ANALYSIS.json. Listener summaries are also parsed. Missing values remain null.

| Field                                    | Exact supplied value                                                      |
| ---------------------------------------- | ------------------------------------------------------------------------- |
| RESULT                                   | `COMPLETE`                                                                |
| INSTALLED_CONTROLLER_SHA256              | `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f`        |
| RUNTIME_IMAGE_ID                         | `sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a` |
| INTERNAL_NETWORK_ID                      | `e94996e300b479ee92c339e460cd408edd48995093f4d5089db44e69515719f3`        |
| GATEWAY_RUNNING_AT_OBSERVATION           | `YES`                                                                     |
| HOST_LISTENER_BEFORE                     | `EXACT_LOOPBACK=0;ANY_IPV4=0;IPV6_LOOPBACK=0;ANY_IPV6=0;TOTAL=0`          |
| HOSTCONFIG_3101_PRESENT                  | `YES`                                                                     |
| HOSTCONFIG_3101_BINDING_COUNT            | `1`                                                                       |
| HOSTCONFIG_OTHER_PORT_KEYS_PRESENT       | `NO`                                                                      |
| HOSTCONFIG_3101_EXACT_LOOPBACK_3101      | `YES`                                                                     |
| HOSTCONFIG_3101_BINDING_01_IP_CLASS      | `IPV4_LOOPBACK_EXACT`                                                     |
| HOSTCONFIG_3101_BINDING_01_HOST_PORT     | `3101`                                                                    |
| NETWORKSETTINGS_3101_PRESENT             | `NO`                                                                      |
| NETWORKSETTINGS_3101_BINDING_COUNT       | `0`                                                                       |
| NETWORKSETTINGS_OTHER_PORT_KEYS_PRESENT  | `NO`                                                                      |
| NETWORKSETTINGS_3101_EXACT_LOOPBACK_3101 | `NO`                                                                      |
| CONTAINER_3101_LISTENER                  | `STATE=LISTEN;TOTAL=1;IPV4=1;IPV6=0`                                      |
| HOST_LISTENER_AFTER                      | `EXACT_LOOPBACK=0;ANY_IPV4=0;IPV6_LOOPBACK=0;ANY_IPV6=0;TOTAL=0`          |
| LOCALHOST_HEALTH_PROBE                   | `URL_ERROR:CONNECTION_REFUSED`                                            |
| FULL_RUNTIME_EXECUTION                   | `NO`                                                                      |
| APP_CONTAINER_STARTED                    | `NO`                                                                      |
| PROXY_CONTAINER_STARTED                  | `NO`                                                                      |
| RAW_GATEWAY_LOG_READ                     | `NO`                                                                      |
| DEPLOY_PATH_USED                         | `NO`                                                                      |
| DEPLOYMENT_REQUEST                       | `NO`                                                                      |
| REPAIR_COUNTER_CHANGE                    | `NO`                                                                      |
| REPAIR_3_AUTHORIZED                      | `NO`                                                                      |
| REPAIR_BUDGET_RESET                      | `NO`                                                                      |
| P2_STARTED                               | `NO`                                                                      |
| PRODUCTION_MAIN_TOUCHED                  | `NO`                                                                      |
| DIAGNOSTIC_GATEWAY_CONTAINER_AFTER       | `ABSENT`                                                                  |
| STAGE3B_CLEANUP_RESULT                   | `PASS`                                                                    |

Missing: raw inspect JSON; diagnostic container ID/exact historical launch command; observation/probe times; socket owner/PID/bind address; Stage3B restart/exit/OOM fields; daemon/network/publication mechanism; original Stage3 checker and Stage2 errno/effective mapping; exact corrective action. No missing value is synthesized from previous executions. Cleanup PASS / diagnostic gateway ABSENT and no app/proxy/full-runtime/deploy-path/request/raw-log/counter/P2/production actions are human attestations, not new host inspection.

## PROPOSED_EXCEPTION_REPAIR — NOT AUTHORIZED

- Exact proven mismatch: correct requested HostConfig binding, absent effective NetworkSettings binding in this isolated Stage3B observation.
- Expected: requested and effective `3101/tcp`, one binding, HostIp127.0.0.1, HostPort3101.
- Observed safe requested value: `IP_CLASS=IPV4_LOOPBACK_EXACT;HOST_PORT=3101`, count1; effective binding absent/count0.
- Component: DOCKER_PORT_PUBLICATION_LAYER; root cause class PROVEN_COMPONENT_CLASS; exact mechanism NOT_ESTABLISHED.
- Smallest repair hypothesis: Make the already requested reviewed 127.0.0.1:3101:3101 binding take effect at the Docker port-publication layer while preserving loopback-only exposure, the internal network and all V4 controls. Evidence does not select a command, source patch or daemon/network intervention.
- Controller source change required: UNKNOWN.
- Docker daemon/runtime configuration change required: UNKNOWN.
- Network change required: UNKNOWN.
- Gateway/image change required: UNKNOWN.
- Security-boundary impact: UNKNOWN until an exact intervention is defined and reviewed. V4 boundaries are unchanged by this recording task.
- New human repair/deployment authorization required: YES.

No patch, command/operator execution recipe, retry or REPAIR_3 is prepared. No source/config/runtime repair is implemented. All future gateway/full-runtime execution, evidence collection, repair/deployment and budget changes remain unauthorized.

## Documentation checks, changed files and stop

23 offline evidence/identity/source checks PASS. These parse the retained handoff and inspect committed source text/AST; no application/runtime tests or live measurements are claimed. Documentation/checksum consistency, byte-identical handoff, prior evidence preservation and Git whitespace are verified before commit. New append-only event0021 equals LATEST_CHECKPOINT.json.

- `.ops/ACTION_REQUIRED.md`
- `.ops/ORCHESTRATOR_STATUS.json`
- `.ops/PROJECT_STATE.md`
- `.ops/PROJECT_STATUS.md`
- `.ops/oversight/LATEST_CHECKPOINT.json`
- `.ops/oversight/LATEST_CHECKPOINT.md`
- `.ops/oversight/events/0021-P1-gateway-stage3b-analysis.json`
- `.ops/reports/P1/CHECKSUMS.sha256`
- `.ops/reports/P1/EVIDENCE.json`
- `.ops/reports/P1/REPORT.md`
- `.ops/reports/P1/gateway-stage3b/ANALYSIS.json`
- `.ops/reports/P1/gateway-stage3b/CHECKSUMS.sha256`
- `.ops/reports/P1/gateway-stage3b/HANDOFF.txt`
- `.ops/reports/P1/gateway-stage3b/REPORT.md`

All prior Stage1/Stage2/Stage3 packages/events, original failures and application/controller/gateway/image/source/tests/dependencies/privileged kit/product documents remain unchanged. Develop only is committed/pushed; main read-only identity remains `c724ac3b50bc44d71f8620bb4ac0cccfae890de2`. INITIAL, REPAIR_1 and REPAIR_2 failed/consumed; repair_cycle2; failed repair cycles2; REPAIR_2 attempts1/1; automatic retries0; budget exhausted. P0 FROZEN/human PASS, P1 BLOCKED/full independent review PENDING; P2–P7 NOT_STARTED; production/main untouched.

PROPOSED_EXCEPTION_REPAIR — NOT AUTHORIZED. Human decision required on the observed requested/effective Docker port-publication mismatch. Exact daemon/network mechanism and intervention remain unknown. Any further evidence collection, gateway/full-runtime execution, repair or deployment requires NEW explicit human authority; no REPAIR_3 or repair-budget extension/reset is authorized.

**NO REPAIR OR DEPLOYMENT IS AUTHORIZED. No further gateway or full-runtime execution is authorized.**
