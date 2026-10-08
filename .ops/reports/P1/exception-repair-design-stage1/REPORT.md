# P1 exception repair design — Stage 1 source review

P1_EXCEPTION_REPAIR_DESIGN_STAGE1_REVIEW_READY: source-only candidate 6726138fc26f883f4782b9113b9aa9eba4cd6730. Local tests:99 Python +9 TypeScript (108 total), PHP lint/stub integration, formatting/lint/typecheck/build PASS; 34 local static-security checklist items PASS. Independent human/ChatGPT source review REQUIRED/PENDING. Candidate removes gateway host-port publication and fixes host ingress at http://172.31.255.2:3101 on gcreation-perf-dev-host-access Internal=true, bridge/local, role dev-host-access, subnet172.31.255.0/29, bridge gateway172.31.255.1, gatewayIP172.31.255.2. App internal-only; proxy internal+egress only; gateway internal+host-access only; builder none. Image/gateway/dependencies unchanged. Host subnet collision status NOT_VERIFIED. No installation, host/network mutation, Docker/runtime/HTTP execution, deployment request, repair or deployment. P1 BLOCKED/HARD_BLOCKED, full independent review PENDING; repair_cycle2/failed cycles2, all INITIAL/REPAIR_1/REPAIR_2 attempts failed/consumed, retries0, budget EXHAUSTED, REPAIR_3 NOT AUTHORIZED, counters unchanged. P0 FROZEN/human PASS; P2–P7 NOT_STARTED; production/main untouched. Stage3B component class DOCKER_PORT_PUBLICATION_LAYER remains isolated evidence; exact daemon/network mechanism and historical exact official REPAIR_2 root cause NOT_ESTABLISHED. STOP. No installation, runtime execution, repair or deployment is authorized.

## Exact identities and authorization

Authorization: **P1_EXCEPTION_REPAIR_DESIGN_STAGE1 — consumed for source review only**. Baseline/parent `ccd31c20a8ec918454aa5aa455972860be17e3bf`; candidate `6726138fc26f883f4782b9113b9aa9eba4cd6730`. Separate checkpoint recording commit follows this candidate; it is not embedded as a self-reference. Original attachment SHA256 `16f2faa42835572442af4f87ac46ee6b85c24b8171484214cff55923f921b4de`; AUTHORIZATION.txt is the same request normalized to LF and is documentary evidence, not execution authority for a server procedure.

Old reviewed/operator-attested installed controller SHA256 `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f`. New candidate controller SHA256 `658ce192284c33b5a211b2a1a5c336bd585f2b1c4518d8f6d0fd4f82026d3bd4`. Installed identity is retained from prior attestation, never freshly inspected. Exact functional diff: SOURCE.patch SHA256 `a3afec1d7b204b5f634b14a71fdef9d350f498ba330fa0a01c064b3d9bba1090`. REVIEW.json records all before/after file hashes. No archive, request, operator installation/refresh recipe or server/network command package is prepared.

## Failure scope and design

Historical Stage2 failed its internal predicate30/30 with URL_ERROR and no status; Stage3B reports correct requested HostConfig loopback3101 and absent effective NetworkSettings port binding, while the container listener was present and localhost connection refused. The proven isolated component class is Docker port publication. The exact daemon/network mechanism and exact historical official REPAIR_2 root cause remain NOT_ESTABLISHED. This candidate follows the newly authorized architecture; it does not manufacture a more specific historical diagnosis.

Before: app={internal}, proxy={internal,egress}, gateway={internal}, builder=none; gateway requested loopback publishing. Candidate: app={internal}, proxy={internal,egress}, gateway={internal,host-access-internal}, builder=none. Gateway publishing is removed entirely. All three network identities/configurations are checked before launch; post-attachment requires exact membership, IDs, immutable image/name/role, no gateway publication, and static host-access address. The old internal-only transitional proxy validation exception is removed, so only complete expected topology is accepted at validation points. The controlled creation sequence still attaches proxy to internal first and then egress, and gateway to internal first and then host-access; no validation accepts those intermediate states.

The dedicated network uses fixed compile-time name gcreation-perf-dev-host-access, Internal=true, bridge/local, exact role dev-host-access, subnet172.31.255.0/29, Docker bridge gateway172.31.255.1, and static gatewayIP172.31.255.2. Network ID is stored under the existing protected STATE identity model as host-access-network-id (64hex exact match/exclusive creation/0600). Host-access IPAM must have exactly one subnet/gateway definition and no extra nonempty range/auxiliary/options/IPv6 configuration. Wrong identities/configuration/members/IP or create failure stop before runtime launch; no alternative subnet or IP exists. Collision freedom and host routing are NOT_VERIFIED.

Docker command semantics in SOURCE.patch: gateway run no longer publishes a host port; a static-IP attachment to the fixed internal host-access network follows launch; all three network validators then require complete membership. These are inert candidate source/mocked argument assertions, not executable operator instructions. All unchanged sandbox/resource/mount/secret/image flags remain byte-identical.

Controller health now uses exactly http://172.31.255.2:3101/health with timeout10; only that expression changes. NoRedirect, HTTP200/service/environment identity, public DEV homepage predicate,30 readiness attempts/sleep2, bounded diagnostics and final-health behavior are retained. The journal predicate label LOCALHOST_ENGINE_HEALTH remains the legacy logical identifier for compatibility; for this candidate only it attributes the fixed private host-access endpoint. Historical records still mean their original localhost transport. No journal schema/serialization or additional retries/fallback are introduced.

WordPress PHP changes only its fixed server-side engine base URL to http://172.31.255.2:3101. Existing path validation, timeout20/redirection0, X-Engine-Secret/X-Client-Key, nonce/session and WooCommerce bytes remain unchanged. Browser/query/options/body inputs cannot override the base. Nginx changes only reviewed explanatory comments and health upstream: exact GET /perf-engine/health, stripped headers/body, empty Content-Length, no master secret and business/admin404 remain byte-identical. The exact private gateway address and both URL forms are rejected by unchanged SSRF policy, including injected redirect tests before second transport.

## Exact candidate changed files

- `ARCHITECTURE.md`
- `SECURITY.md`
- `docs/DEV_VALIDATION_RUNBOOK.md`
- `ops/dev/HUMAN_PLUGIN_ARTIFACT.md`
- `ops/dev/README.md`
- `ops/dev/deploy_controller.py`
- `ops/dev/nginx-dev.conf.example`
- `tests/foundation.test.ts`
- `tests/test_controller_health_diagnostics.py`
- `tests/test_deployment_kit.py`
- `tests/test_host_access_network.py`
- `tests/test_security_review_v3.py`
- `tests/test_security_review_v4.py`
- `tests/wordpress-integration.php`
- `wordpress/gcreation-performance/gcreation-performance.php`

Functional changes are only the three authorized source files; seven tests (one new) and five active design documents support them. REFERENCES.json classifies all49 baseline localhost occurrences; historical evidence, unrelated loopback fixture and locked MASTER_PRODUCT_SPEC are preserved. The later explicit Stage1 human exception narrowly overrides candidate host transport in active design documentation without rewriting the master specification. Prior install/runbook recipes remain historical/future-only and grant no authority; no new runtime/installation recipe is provided.

## Local verification

| Command | Result | Count |
| --- | --- | --- |
| `python3 -B tests/test_host_access_network.py -v` | PASS | 24 |
| `python3 -B tests/test_controller_health_diagnostics.py -v` | PASS | 22 |
| `python3 -B tests/test_deployment_kit.py` | PASS | 12 |
| `python3 -B tests/test_security_review_v3.py` | PASS | 21 |
| `python3 -B tests/test_security_review_v4.py` | PASS | 13 |
| `python3 -B tests/test_source_permissions.py` | PASS | 3 |
| `python3 -B tests/test_installer_bytecode.py` | PASS | 4 |
| `.ops/toolchain/node_modules/node/bin/node --import tsx --test tests/foundation.test.ts` | PASS | 9 |
| `php -l wordpress/gcreation-performance/gcreation-performance.php` | PASS | check/contract |
| `php tests/wordpress-integration.php` | PASS | check/contract |
| `scripts/npm-dev.sh run format:check` | PASS | check/contract |
| `scripts/npm-dev.sh run lint:ts` | PASS | check/contract |
| `scripts/npm-dev.sh run typecheck` | PASS | check/contract |
| `scripts/npm-dev.sh run build` | PASS | check/contract |
| `scripts/repo-git.sh diff --check` | PASS | check/contract |

99 Python +9 TypeScript tests PASS, zero failures. PHP lint and stub commerce/host-routing contracts PASS (the harness does not expose a numeric assertion count). Targeted topology suite ran first. Full npm test/gateway socket tests were deliberately not executed because Stage1 forbids HTTP/runtime probes. All network/command inspections are strict mocks; SSRF DNS/transport are injected. Source-only offline TypeScript compilation/build executes no app/gateway runtime. These local results do not prove Docker/kernel/network/cgroup/WordPress/Plesk/nginx or real DEV acceptance. Ordinary UID was10023. No dependencies installed or fetched.

Additional byte/data audit:16 unchanged controller function/class bodies, health identical after endpoint substitution, deploy identical after one host-access prebuild check, PHP exact endpoint substitution, nginx boundary equality,237 other baseline tracked files unchanged before checkpoint work. REVIEW.json maps all35 required regressions to actual tests/byte checks. Final governance/history preservation checks are recorded by the checkpoint transaction.

## Dedicated local static/security checklist

All results below are local source review only; **independent human/ChatGPT review remains REQUIRED**, not PASS.

| # | Item | Result | Evidence finding |
| --- | --- | --- | --- |
| 1 | Docker host port publication removed | PASS | Gateway argv has no -p/--publish; HostConfig and effective Ports inspection reject all nonempty bindings. |
| 2 | Dedicated host-access network Internal=true | PASS | Fixed ensure_host_access_network supplies True; incorrect flag fails before launch. |
| 3 | Exact driver/scope/label | PASS | bridge/local and exactly gcreation.role=dev-host-access required. |
| 4 | Exact fixed subnet | PASS | Compile-time 172.31.255.0/29; exact create argument and IPAM check. |
| 5 | Exact fixed bridge gateway | PASS | Compile-time 172.31.255.1; exact create and IPAM check. |
| 6 | Exact gateway container IP | PASS | Compile-time 172.31.255.2; static attachment, endpoint IP/prefix and member IPv4Address required. |
| 7 | Dynamic fallback absent | PASS | One fixed subnet/IP/endpoint. Docker creation failures propagate without alternative or allowed failure. |
| 8 | Persisted network identity enforced | PASS | Existing STATE identity file uses exact 64-hex ID, exclusive creation and 0600; STATE root-private ownership is the unchanged installed trust assumption, not newly measured. |
| 9 | Unexpected host-access members rejected | PASS | Only fixed gateway allowed; names/IDs/roles/image validated. |
| 10 | Gateway exactly two internal networks | PASS | Exact set {internal,host-access}; preflight rejects incomplete existing topology and post-attachment requires full membership. |
| 11 | Gateway external egress absent | PASS | Extra egress/bridge/host/unrelated attachments fail closed. |
| 12 | Proxy sole egress holder | PASS | Exact proxy internal+egress; gateway/app cannot join egress; egress membership allows only proxy. |
| 13 | App no host-access attachment | PASS | Exact app internal-only. |
| 14 | Builder network=none | PASS | build_command byte-equal; existing sandbox/offline baseline maintained. |
| 15 | Default bridge rejected | PASS | Every valid runtime member requires exact network set; Docker run supplies fixed internal network. Builder has network=none. |
| 16 | Health acceptance semantics unchanged | PASS | health byte-equal after only endpoint substitution; HTTP200/service/environment, homepage ordering, exceptions, final semantics preserved. |
| 17 | Health retry/timeouts unchanged | PASS | 30 attempts, 2-second sleep, timeout10 internal /15 homepage; exact old readiness tail retained. |
| 18 | No localhost fallback | PASS | One ENGINE_HOST_URL; no former endpoint anywhere in controller functional source. NoRedirect class byte-equal. |
| 19 | WordPress secret boundary unchanged | PASS | PHP bytes differ only by fixed endpoint; server X-Engine-Secret and X-Client-Key/timeout20/redirection0/path/nonce/session/commerce unchanged. |
| 20 | Browser cannot control engine endpoint | PASS | Fixed literal URL; invalid absolute/query paths do not reach stub; query/options/body engine URL cannot alter target. |
| 21 | Public nginx health-only | PASS | Only GET /perf-engine/health; input headers/body off, Content-Length empty, no master secret; other engine namespace404. Body byte-equal after upstream substitution. |
| 22 | Private IP remains SSRF-blocked | PASS | Exact IP and URLs with/without3101 denied before DNS, redirects denied before second transport. No policy edit or whitelist. |
| 23 | No new credentials | PASS | Existing three fixed secrets unchanged; no request schema/env field added; trusted constants not developer-configurable. |
| 24 | No raw secret logging | PASS | emit_health_diagnostic and command byte-equal; new validation messages are fixed strings only. |
| 25 | No image/trusted gateway modification | PASS | gateway hash matches prior reviewed source; Dockerfile/prepare/install/source dependency inputs byte-equal. Gateway already listens0.0.0.0:3101 and fixed internal upstream unchanged. |
| 26 | No dependency changes | PASS | package.json/package-lock.json byte-equal, no npm install/ci executed. |
| 27 | Rollback topology consistent | PASS | Existing deploy rollback calls same start_runtime; only added host-access prebuild check in deploy. |
| 28 | Network mismatch fails closed | PASS | ID/config/IPAM/staticIP/role/member errors propagate before startup; postattachment mismatches prevent health acceptance. |
| 29 | Historical evidence preserved | PASS | All prior Part packages/events/source not in allowlist byte-equal; report only prepended; existing EVIDENCE entries/objects preserved. |
| 30 | Production/main untouched | PASS | No production configuration/hostname behavior changed; remote main remains c724ac3b50bc44d71f8620bb4ac0cccfae890de2. No production/runtime request. |
| 31 | No privileged/runtime action performed | PASS | Ordinary UID10023; strict mock boundaries; Python fixture/TS injected transport/PHP stubs and compilers only. No root/Docker/systemd/Plesk/HTTP commands. |
| 32 | REPAIR_3 false | PASS | No REPAIR_3 authorization/request/execution. |
| 33 | Repair budget unchanged | PASS | repair_cycle2/failed cycles2, INITIAL/REPAIR_1/REPAIR_2 consumed, retries0, exhausted. Stage1 source review authorization consumed separately. |
| 34 | P2 NOT_STARTED | PASS | P2–P7 remain NOT_STARTED; P0 FROZEN/humanPASS. |

## Security impact and STOP

The source candidate changes trusted controller topology and private host ingress routing under the explicit design authorization. It preserves the V4 enforcement model: image-baked immutable proxy/gateway, frozen dependency/offline build, root snapshot/archive/request trust, root-persisted network IDs, strict membership/static addressing, proxy-only egress, SSRF denial, distinct secrets, health-only public nginx, human-only PHP, unchanged sandbox/cgroups/resource limits, rollback path and bounded logs/retention. Real host privileges/state and installed boundaries are unchanged. This is a design review candidate, not a security approval or runtime repair execution.

Runtime image remains prior operator-attested `sha256:c1ab6bc3d731e10291b1f81965e20936a28cfba73378a1af551c913e184bea4a`; image change required NO. Trusted gateway source hash remains `d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c`; it already listens0.0.0.0:3101 and uses fixed internal app upstream. Dockerfile/prepare/installer/preflight, gateway, proxy/scanner/app/database/business code, dependencies, systemd/seccomp and production configuration are unchanged. No host lookup or live file was inspected to reverify these installed claims.

EXCEPTION_REPAIR_DESIGN_STAGE1_AUTHORIZED=true; EXCEPTION_REPAIR_DESIGN_STAGE1_COMPLETE=true; SOURCE_CANDIDATE_ONLY=true; HOST_MUTATION=false; RUNTIME_EXECUTION=false. Candidate installed=false; runtime validated=false; repair executed=false; Docker execution=false; deployment request=false; deployment authorized=false; REPAIR_3=false; repair counters unchanged; budget exhausted=true. P1 remains BLOCKED/HARD_BLOCKED; P2–P7 NOT_STARTED; production/main untouched. Next action: independent source review only. **NO INSTALLATION, RUNTIME EXECUTION, REPAIR OR DEPLOYMENT IS AUTHORIZED.**
