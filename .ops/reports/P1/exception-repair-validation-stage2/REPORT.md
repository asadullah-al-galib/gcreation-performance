# P1 exception repair validation Stage2 — evidence and acceptance assessment

**Stage2 controlled transport validation PASS; full P1 final acceptance NOT_READY.** P1 stays HARD_BLOCKED/BLOCKED, full independent review PENDING. This task only ingests evidence, analyzes committed requirements, records governance and pushes develop. No code, runtime, HTTP, privileged or deployment action is performed or authorized.

## Exact evidence and identity

Baseline checkpoint `e5ca71c1e35da57c963f01d4ad10830016542fd4`; source/controller candidate `6726138fc26f883f4782b9113b9aa9eba4cd6730`. At entry local HEAD, tracking develop and independently read remote develop all equal the baseline; tree clean, branch develop. Remote main remains `c724ac3b50bc44d71f8620bb4ac0cccfae890de2`; no local origin/main assumption. Source candidate/parent/checkpoint graph and exact controller bytes were verified through scripts/repo-git.sh.

HANDOFF.txt is byte-identical to `/home/codexperf/p1-exception-validation-stage2-v4.txt`: SHA256 `27ceff5b9a28f71a5d132682ac04e6310598fb172ff1bae05347e356888d5e94`,2554 bytes. SHA/size both match the explicit handoff identity. No substitute handoff was read. Human request SHA256 `5ece1e0d5dacfd3d13b597e4c21b93bc76b2ea688221370d1315aaeffe7ad229`; AUTHORIZATION.txt retains the request with LF normalization and is documentation only.

New installed controller hash `658ce192284c33b5a211b2a1a5c336bd585f2b1c4518d8f6d0fd4f82026d3bd4` equals reviewed Git/local candidate. Previous operator-attested controller hash `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f` equals the prior Stage1 reviewed parent. Installation is **EXACT_REVIEWED_CANDIDATE_INSTALLED, operator-attested**. Codex did not read the installed root file or verify root ownership/mode/link/backup/ancestors. Those facts are absent, not invented.

Preserved release `release-1791293466993919` and source snapshot `44b5b3b45036ce787f2b9c4ecb20ae21c37db323904b6f18c7c341b976d528ae` are operator-attested. The digest matches the accepted application source `0ac34ba50ab3192abfe2ae425c4283879484258e` / prior archive `958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced` and image Gate C record. Stage2 reused preserved runtime output; it did not deploy candidate6726138 mutable workspace/archive bytes. Runtime image ID `sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a` matches the accepted promoted immutable image. Per-container running image/ID outputs and protected release/output bytes are not supplied/read.

## Full handoff parsing and safe holds

All 67 lines are retained, including the heading, 64 key/value occurrences representing 58 unique keys, 2 readiness summaries and the original newline termination. All 6 duplicate field names have consistent values; none is silently overwritten. ANALYSIS.json stores every occurrence with its original line number/value, canonical fields, duplicate records, typed readiness events and all 155 offline document/Git consistency checks. All supplied values were parsed; absent timestamps, commands/exit codes, inspect details and response version/body stay null/not supplied. These checks verify evidence consistency, not 155 runtime tests.

V1 handoff reference `ad3c330676ae7de2e5e634c05e2ae285eca949b9e3a2e64b1226b9167324715c`, V2 `2c57b4c18ef20c8dc121c8145df3a04cf941a241bae7962f7ab9fcf726eeea02`, V3 `8763a312f5d5028efc5922e0f2638c56a838b28679926def8dbed9e30815c4a2` each have STOPPED_PRE_MUTATION=YES. These are verified references and operator attestations within V4 only; original V1/V2/V3 files were not read or independently hashed. They remain historical safe holds, never repair attempts, retries or failed cycles. Only the successful V4 controlled execution is counted, count 1, as explicitly reported by the human. Readiness probes are not multiple executions.

## Controlled runtime and reachability

| Readiness attempt | Private engine | DEV homepage |
| --- | --- | --- |
|01 | FAIL, URL_ERROR, no HTTP status | NOT_REACHED |
|02 | PASS, OK, HTTP200 | PASS, OK, HTTP200 |

The 3 event/1 private PASS/1 private FAIL/1 homepage PASS/0 homepage FAIL counts and URL_ERROR:1/NONE:1 distributions reconcile exactly. This agrees with the candidate's sequential private engine then homepage health flow and bounded readiness loop. The first private failure's underlying detail is not supplied: no startup-race/DNS/daemon diagnosis is invented. Automatic deployment retries remain0.

Private controller target is fixed http://172.31.255.2:3101/health; its reviewed health predicate requires HTTP200/service=gcreation-performance/environment=development, with NoRedirect. The legacy logical label LOCALHOST_ENGINE_HEALTH remains in source; the handoff attributes it as PRIVATE_ENGINE. DEV_HOMEPAGE means https://dev.gcreation.agency/ and does not mean the public engine-health route. The unchanged gateway forwards to the fixed internal app upstream, so reported private health supports the gateway-to-app health path; this is a source-supported inference from the attested result, not an agent socket trace. No structured version response or observation timestamp is retained.

| Technical item | Classification |
| --- | --- |
| exception_repair_source_candidate | VALIDATED_IN_ONE_CONTROLLED_DEV_RUNTIME |
| collision_preflight | PASS_OBSERVED |
| controller_installation | EXACT_REVIEWED_CANDIDATE_INSTALLED |
| host_access_network | EXACT_CONFIGURATION_VALIDATED_OPERATOR_ATTESTED_SUMMARY |
| docker_host_port_dependency | REMOVED_IN_VALIDATED_RUNTIME |
| private_host_to_gateway_path | PASS_OBSERVED |
| gateway_to_app_health_path | PASS_OBSERVED |
| dev_homepage_health | PASS_OBSERVED |
| php_site_user_cli_to_gateway | PASS_OBSERVED |
| php_fpm_context | NOT_PROVEN |
| nginx_worker_to_gateway | PASS_OBSERVED_STANDALONE_ONLY |
| actual_plesk_vhost_configuration_validated | NOT_PROVEN |
| actual_wordpress_plugin_applied | NO |
| proxy_only_egress | OPERATOR_SUMMARY_ATTESTED; EXACT_TOPOLOGY_EVIDENCE_NOT_RETAINED |
| controlled_runtime_cleanup | PASS_OBSERVED |
| standalone_nginx_cleanup | PASS_OBSERVED |
| dev_runtime_containers_after | ABSENT_OPERATOR_ATTESTED |
| host_access_network_retained | YES_OPERATOR_ATTESTED |
| repair_hypothesis | VALIDATED |
| historical_official_repair_2 | FAILED_CONSUMED_1_OF_1 |
| historical_exact_repair_2_root_cause | NOT_ESTABLISHED |
| stage3b_component | DOCKER_PORT_PUBLICATION_LAYER |
| stage3b_proof_scope | ISOLATED_DIAGNOSTIC_COMPONENT_CLASS_ONLY |
| stage3b_exact_daemon_network_mechanism | NOT_ESTABLISHED |

Host-access name gcreation-perf-dev-host-access, subnet172.31.255.0/29, bridge gateway172.31.255.1 and gatewayIP172.31.255.2 match the reviewed compile-time constants; collision preflight/network create/validation are reported PASS. Driver/scope/Internal/labels/IPAM/persisted network ID and per-container exact network sets/IDs are not returned. Therefore proxy-only egress is **summary-attested, not promoted to direct exact-topology acceptance** merely from PROXY_ONLY_EGRESS=YES/RUNTIME_TOPOLOGY=PASS. Static strict topology checks remain valid source evidence, not live inspection results.

PHP site-user CLI reachability and standalone nginx worker reachability/cleanup are PASS_OBSERVED. PHP_FPM_CONTEXT_PROVEN=NO; actual WordPress plugin and Plesk nginx config were not mutated. Standalone worker success is not actual configured public-vhost acceptance. Runtime cleanup PASS and DEV_RUNTIME_CONTAINERS_AFTER=ABSENT are operator observations; host-access network remains retained. No agent cleanup or host action occurred, and no bounded-retention/rollback proof is inferred from cleanup.

## Part boundaries and integration limitations

| Supplied limitation | Classification | Committed requirement interpretation |
| --- | --- | --- |
| PHP_FPM_CONTEXT_PROVEN=NO | P3_REQUIRED | Actual approved PHP plugin/nonce-session/engine customer flow and PHP-owner/config readability belong to P3. Site-user CLI reachability does not prove FPM, but P1 does not require plugin/customer PHP execution. This is a P3 integration inference from the committed actual-flow requirement, not a new standalone FPM configuration test. |
| ACTUAL_WORDPRESS_PLUGIN_MUTATED=NO | P3_REQUIRED | Separately approved plugin artifact installation/activation/readability and working customer flow are P3, not the watcher/P1. Mutation itself is not a required success flag if an already approved exact plugin is installed; this handoff only says it was not changed. |
| ACTUAL_PLESK_NGINX_CONFIG_MUTATED=NO | NOT_REQUIRED_FOR_P1 | Config mutation is not an exit criterion; a working existing approved vhost could satisfy D26 unchanged. Actual public /perf-engine/health and404/boundary proof are explicitly P1. Standalone nginx PASS does not establish that proof; it is not deferred as P3 customer integration. |

P3 scope/entry/DEV/exit and REQUIREMENTS D15 assign actual approved plugin/PHP customer-flow integration to P3. P1 has no plugin-installation or FPM customer-flow exit. The literal nginx mutation flag is NOT_REQUIRED_FOR_P1 because configuration need not be changed if already correct; **actual public health-only route acceptance is P1_REQUIRED by D26**. Thus missing public health cannot be shifted into P3. P2 browser/Lighthouse/discovery/job measurements and P3 customer/commerce flows are not added as P1 blockers. No Part scope or exact exit is rewritten.

## P1 acceptance assessment against committed exits

PROJECT_TIMELINE P1 requires successful constrained offline deploy/status with archive/snapshot, direct runtime boundary proof, structured internal/public health identity, public forbidden-route refusal and controlled retention. P0.2 section19 explicitly retains effective identity/topology/secrets/non-root/seccomp/resources/public route/request/release/evidence requirements. REQUIREMENTS D24–D27 are P1-owned. Stage2 is positive foundation evidence; it does not replace those exits. Full P1 technical execution is not PASS, and P1_FINAL_ACCEPTANCE_REVIEW_READY=false.

| # | Genuinely P1-scoped missing evidence | Exact gap | Authority |
| --- | --- | --- | --- |
| 1 | D24 / successful constrained offline deployment | Successful terminal deploy/status and release/archive/snapshot association. No new build/deployment is authorized by this analysis. | PROJECT_TIMELINE.md: P1 exact exit/evidence criteria, REQUIREMENTS.md: D24, docs/P0_2_AUTONOMOUS_AUTHORIZATION.md: section19 |
| 2 | P1 trust/network/secret/sandbox boundaries and D27 effective limits | Exact live topology/identity and effective trust/containment/resource observations; summaries or source flags alone cannot satisfy P1/D27. Real browser/Lighthouse work remains P2/P5, not this P1 missing item. | PROJECT_TIMELINE.md: P1 requires real DEV validation/exact exit, REQUIREMENTS.md: D27, docs/P0_2_AUTONOMOUS_AUTHORIZATION.md: section19 |
| 3 | D25 complete structured internal-health identity evidence | Retained structured health/version evidence linked to that runtime/source observation. This does not invalidate the observed private path/health PASS. | PROJECT_TIMELINE.md: P1 exact exit/evidence criteria, REQUIREMENTS.md: D25 |
| 4 | D26 actual public DEV health and forbidden engine routes | Actual public vhost health and forbidden-route/boundary observations. A config mutation is not itself mandatory if existing approved config satisfies the criterion; these acceptance checks are P1, not P3. | PROJECT_TIMELINE.md: P1 internal/public health exit, REQUIREMENTS.md: D26, docs/P0_2_AUTONOMOUS_AUTHORIZATION.md: section19 |
| 5 | P1 controlled retention / bounded evidence / stale-request behavior | Controlled retention/bounded evidence and stale-request refusal proof. Cleanup PASS is not retention/rollback proof. Restoration to an earlier successful runtime is separately DEFERRED per P0.2 section19 and is not used as a current blocker. | PROJECT_TIMELINE.md: P1 real DEV/exit criteria and P0.2 amendment, REQUIREMENTS.md: D24, docs/P0_2_AUTONOMOUS_AUTHORIZATION.md: section19 |

| P0.2 section19 criterion | Assessment | Evidence or limitation |
| --- | --- | --- |
| Accepted controller repair installed correctly | PARTIAL_OPERATOR_ATTESTED | Exact candidate bytes/hash installation PASS; ownership/mode/link/ancestors/backup details not retained. |
| Approved immutable runtime identity used | PASS_OPERATOR_ATTESTED_ID | RUNTIME_IMAGE_ID equals accepted promoted image; per-container IDs/image bindings not retained. |
| Constrained non-root build succeeds | PRIOR_INFERRED_EXIT_ZERO; EFFECTIVE_PROOF_PENDING | Prior REPAIR_2 reached runtime-health after build return0. Stage2 executes preserved output, not build/deploy; sandbox/builder direct evidence absent. |
| Application starts | PASS_OBSERVED | APP_RUNNING=YES and upstream private health PASS; operator attestation. |
| Expected container identities | NOT_VERIFIED | Exact IDs/names/roles/per-container image identities not supplied. |
| Expected dedicated network membership | SUMMARY_ONLY | RUNTIME_TOPOLOGY=PASS/PROXY_ONLY_EGRESS=YES; exact sets/IDs/Internal/config outputs absent. |
| No inappropriate direct egress | SUMMARY_ONLY | Proxy-only summary YES; no direct exact topology proof retained. |
| Expected secret separation | NOT_VERIFIED | No recipient/permission/self-host deny/env ownership observations retained; no secret values requested. |
| No secret exposure in evidence/logs | PASS_SANITIZED_HANDOFF; RUNTIME_LOG_SCOPE_PENDING | Supplied handoff has status/identity metadata only; actual credential/environment or live logs not read. |
| Expected UID/GID | NOT_VERIFIED | Effective runtime10001:10001 not supplied. |
| Cap drop | NOT_VERIFIED | No effective ALL-drop observation. |
| No new privileges | NOT_VERIFIED | No effective value supplied. |
| Seccomp | NOT_VERIFIED | No effective seccomp observation. |
| PID limit | NOT_VERIFIED | No effective container/slice PID observations. |
| CPU/memory limits | NOT_VERIFIED | No effective per-container/build limits. |
| Aggregate slice limits | NOT_VERIFIED | No effective slice CPU/memory/tasks evidence. |
| Internal health works | PASS_OBSERVED_CONTROLLED_SCOPE | Attempt02 PASS:OK:200; raw structured version/body not retained for complete D25. |
| Allowed public health route works | NOT_VERIFIED | Homepage GET / and standalone proxy do not establish actual /perf-engine/health. |
| Forbidden/admin paths not public | NOT_VERIFIED | No actual public404/boundary observations supplied. |
| Request consumed exactly once | PASS_PRIOR_OFFICIAL_REPAIR2_ONLY | Prior exact one-shot request consumed once, final claim/request absent. Stage2 request count0, not a replacement deployment. |
| Release identity persisted | PARTIAL_OPERATOR_ATTESTED | Preserved release name and matching prior source snapshot supplied; no successful deployed release/status association. |
| Retained evidence bounded | NOT_VERIFIED | Cleanup assertions/preserved release do not supply effective retained count/bounds. |
| No production touched | PASS_OPERATOR_SCOPE_AND_GIT | Operator flag NO; agent evidence/Git only, remote main unchanged; no production inspection. |

Earlier reviewed-root installation, repaired image promotion, dependency baseline, one-shot request consumption and inferred old build completion are preserved with their own scope; no valid work is reset. Historical REPAIR_2 watcher status remains FAILED/runtime-health, rollback=false, consumed1/1. No successful official status/active release is manufactured from Stage2; OFFICIAL_DEPLOYMENT_REQUEST=NO and DEPLOY_FUNCTION_CALLED=NO.

First-runtime restoration to an earlier working runtime stays **DEFERRED/PENDING under P0.2 section19**, excluded from this missing-criteria block. Actual retention/stale-request evidence is not covered by that exception. No successful restoration is invented, no third request or runtime validation is proposed, and the missing list is an evidence assessment only. Human/ChatGPT final acceptance decision remains required; this package is ready for that decision, while full P1 acceptance-review readiness is NOT_READY under unchanged technical gates.

## Historical mechanism and governance

Repair hypothesis VALIDATED: the replacement architecture avoids gateway host-port publication dependency in one controlled DEV runtime. It does not prove the exact historical Docker daemon/network mechanism. Historical official REPAIR_2 exact underlying root cause remains NOT_ESTABLISHED; isolated Stage3B component class DOCKER_PORT_PUBLICATION_LAYER remains unchanged.

EXCEPTION_REPAIR_VALIDATION_STAGE2_AUTHORIZED=true; COMPLETE=true; RESULT=PASS; CONTROLLED_RUNTIME_EXECUTION_COUNT=1; OFFICIAL_DEPLOYMENT_ATTEMPT=false record completed human action only, not future authority. INITIAL/REPAIR_1/REPAIR_2 remain FAILED/CONSUMED; repair_cycle2, failed cycles2, retries0, repair budget EXHAUSTED, REPAIR_3 false. P0 FROZEN/humanPASS; P1 BLOCKED/HARD_BLOCKED/full independent review PENDING; P2–P7 NOT_STARTED; production/main untouched. Codex performed read-only sanitized evidence/source/Git analysis and project-local governance writes only. No Docker/HTTP/PHP/nginx/systemd/root/Plesk/WP execution, controller installation, source/test/dependency/kit changes, request, deploy(), cleanup or deployment occurred.

Final current checkpoint/event records these findings; all prior report/package/event bytes remain immutable. Commit/push develop only, then verify clean tree and HEAD=origin/develop. No guessed/self-referencing checkpoint SHA is embedded in this package.

**NEXT ACTION: FINAL P1 ACCEPTANCE DECISION REQUIRED. NO DEPLOYMENT, REPAIR_3, P2 OR PRODUCTION ACTION IS AUTHORIZED.**
