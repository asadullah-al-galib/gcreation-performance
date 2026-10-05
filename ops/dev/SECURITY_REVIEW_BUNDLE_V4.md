# Fourth human security review bundle

STATUS: READY FOR FOURTH SECURITY REVIEW — HOLD.

Do not install or execute privileged components, create a deployment request or claim DEV deployment complete. This handoff stops at review. Production was not accessed or modified. The third-review findings are preserved in docs/THIRD_SECURITY_REVIEW_RESULT.md; V2/V3 history and accepted controls are preserved.

## Exact identities and reproducibility

Source commit: `8217aa4a13c0265efd8cb81473dd7f00c68d2c34` on develop, descendant of V3 handoff `02edd2da5a491ce5b882883ff4aab2a2a1e7f768` and original reviewed7887fca.

Source archive: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-8217aa4a13c0265efd8cb81473dd7f00c68d2c34.tar.gz`.

Archive SHA-256: `ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7`.

The archive contains81 committed regular files plus REVIEW_SOURCE_COMMIT (82 entries). Two independent exports produce identical bytes. Every regular member matches its committed Git blob; the marker matches the source commit. No symlinks, hardlinks, special files, unsafe paths or secrets are included. Export fixes ordering, tar format, mode, ownership, timestamps and gzip metadata. Source snapshots and tests are ordinary-user operations inside the project.

Handoff commit: the metadata-only child of this source commit containing the five files listed below; its exact ID is provided with the final handoff and can be obtained from `scripts/repo-git.sh log -1 --format=%H`. It cannot be embedded inside its own committed contents. All privileged/runtime inputs remain byte-identical to source. The source archive records preparation-time state; current ACTION_REQUIRED/PROJECT_STATE/MASTER_EXEC_PLAN are handoff state and are excluded from the immutable source manifest.

V4 manifest contains78 immutable source files, covering all privileged/root/Docker-influencing inputs below and the complete remaining source/tests/configuration. Only the three mutable state ledgers are excluded. New V4 bundle/manifest are handoff metadata excluded to avoid self-reference. Historical V2/V3 manifests are archived evidence; their old source hashes are not expected to describe the current source tree. Verify current candidate with V4.

## Remediation boundaries

1. Trusted egress proxy and security policy compile from explicit reviewed snapshot files into `/opt/gcreation-trusted/dist` during human image installation. The gateway is also baked into that image. Trusted containers have no release/source/data bind mounts, use readonly image roots and non-root UID/GID10001. Autonomous releases cannot replace their executable code/policy. Trusted policy updates require a new human review/image.
2. Only reviewed package manifests are present during `npm ci --ignore-scripts`; no source/lifecycle/test/build script runs in that networked image step. Reviewed trusted TypeScript compile runs with Dockerfile `RUN --network=none`; BuildKit is required. Installed package.json/package-lock.json SHA-256 baseline and immutable Docker image ID are root-owned. Image ID covers the complete locked dependency set and compiled enforcement code. Autonomous manifest changes fail before build; dependency updates require a reviewed image.
3. Future untrusted source builder runs `--network=none`, without credentials, with readonly source/image, writable bounded release output and frozen image dependencies linked into node_modules. Source format/TypeScript lint/typecheck/Node tests/build run offline. PHP/Python/shell/security-review checks run separately as ordinary-user review gates. The image does not add PHP or give npm scripts network access.
4. APP/GATEWAY attach only to dedicated Internal=true `gcreation-perf-dev-internal`. PROXY alone also attaches to dedicated Internal=false `gcreation-perf-dev-egress`. No container uses default bridge. Exact name/ID/driver/local scope/role-label/Internal and attachment membership are verified before and after runtime start. Named members must match inspected container IDs, role, immutable image ID and expected network set. Persisted network IDs fail on replacement. Unexpected containers fail closed.
5. Browser → WordPress nonce/session PHP → trusted localhost gateway → mutable internal app. ENGINE_SECRET exists only in trusted gateway and separately approved WP config0600; APP_GATEWAY_SECRET goes only to gateway/app; FETCH_PROXY_SECRET only to app/fetch proxy. All three differ. Root provisioners validate/split configuration into separate state env files0600, never argv/logs. Proxy and app never receive ENGINE_SECRET. Gateway strips incoming credentials, injects the hop secret, forwards only validated client keys and response content type, rejects redirects and bounds requests/connections/deadlines/responses.
6. Preflight uses bounded isolated system-Python DNS for dev.gcreation.agency only. Every current public answer plus103.112.63.86 must be configured in root DENIED_IPS. Missing/empty answers fail. The immutable policy also unconditionally denies raw103.112.63.86. DEV/production hostnames, private/link-local/metadata/reserved/mapped addresses remain blocked; DNS and every redirect are validated and pinned; browser/Lighthouse egress remains proxied. IPv6 deny matching is normalized. No production connection or lookup is made.
7. Future requests require exact action/commit/archive_sha256 schema and fixed `.ops/source-artifacts/<commit>.tar.gz`. The root watcher reads one bounded anchored regular byte sequence as DATA, verifies hash, bounded gzip/tar paths/types/file counts/bytes and marker, then frozen manifest hashes. It never executes source on the root host or copies current workspace bytes. Archive SHA is canonical deployed byte identity; commit marker is exporter-declared identity, not a signed Git provenance assertion. Active/status evidence includes commit, archive SHA and canonical snapshot SHA. Requests are atomically claimed; only the claimed request is removed.
8. Future root interpreter commands require env -i with fixed system PATH, preserving Python -I. The reviewed installer executes only from the validated root-owned hash-bound snapshot; isolated watcher adds only validated installed trusted modules. No inherited BASH_ENV/PYTHONPATH can alter startup under the documented recipe. Do not run those future recipes at this checkpoint.

Accepted controls remain: safe reviewed archive/root snapshot transition; stale-trigger preflight before any installation and before watcher enable; human-only WP artifact that drops root before fixed DEV writes and creates config0600; public GET health-only nginx without client headers/body or engine business routes; digest-pinned official image references/seccomp; no Docker socket/group/Plesk/root-host mounts; non-root capability drop/no-new-privileges/read-only mounts/PID192/container; bounded tmpfs/logs/source artifacts/retries/retention; concurrency1; rollback/three releases including failed attempts; no paid AI dependency. Resource ceilings remain4CPU/1700MiB/TasksMax256 aggregate, with app3.4CPU/1400MiB, proxy0.5CPU/150MiB, gateway0.1CPU/100MiB, and builder3.5CPU/1500MiB while runtime is stopped.

## Complete non-privileged results

| Gate | Workspace | Fresh canonical archive extraction |
| --- | --- | --- |
| Exact Node24.21.0 clean npm ci --ignore-scripts | PASS (295 packages) | PASS, offline cache install (295 packages) |
| format:check | PASS | PASS |
| lint: ESLint + Python + PHP + shell | PASS | PASS |
| Original Python deployment boundaries | 12/12 PASS | 12/12 PASS |
| Prior V3 Python regressions | 21/21 PASS | 21/21 PASS |
| New V4 Python trust/network/artifact regressions | 13/13 PASS | 13/13 PASS |
| TypeScript typecheck | PASS | PASS |
| TypeScript feature/SSRF/scanner/UI tests | 26/26 PASS | 26/26 PASS |
| Trusted gateway real loopback socket tests | 4/4 PASS | 4/4 PASS |
| PHP syntax + WooCommerce/security contract | PASS | PASS |
| bash/sh syntax | PASS | PASS |
| Application build | PASS | PASS |
| Trusted proxy-only compilation with reviewed config | PASS | PASS |
| npm dependency audit | 0 vulnerabilities | Uses identical locked dependency set |
| Git diff whitespace check | PASS | Committed source verified |
| Deterministic export, safe members, exact committed bytes | PASS | 82/82 regular entries match |
| Immutable source manifest | 78/78 SHA-256 match | All source bytes verified |

No tests failed, were skipped or cancelled in the final suites. Final source review comprises46 Python and30 Node tests; reruns are not additional tests. V4 tests exercise trusted command/mount isolation, frozen dependency preparation, offline builder/no credentials, dedicated network identity/foreign members/impersonation/default bridge rejection, distinct env ownership0600, self-host and all-DNS deny requirements, bounded isolated DNS child, archive hash/marker/snapshot/workspace independence, dependency changes/unsafe paths/links/special inputs, old request schema rejection and clean root commands. Prior V3 tests remain and pass with fixtures updated for the stronger request/secret contract. Existing features were retained.

Complete fresh-source gate output: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/V4_SOURCE_VALIDATION.log`.

Validation log SHA-256: `8b8b3548ddad7bcac2987026998542cde3fb10f704587256fd7f2cbcc3e4b260`.

These results prove local observed behavior and mock boundary contracts. They do not prove installed Docker routing, cgroups, sandbox, real Chromium/Lighthouse, runtime readiness, public DEV deployment, WordPress activation/payment or controlled-site E2E. No Docker/root/systemctl/Plesk command was executed by the agent. Tests that simulate root observations do not change the actual process UID. No deployment trigger exists from this work. DEV deployment remains incomplete.

## Exact files to provide to the human reviewer

Provide these five files plus the exact source/handoff commit IDs. The archive contains every reviewed source/input; no runtime.env/config.php/token/customer data is included:

- `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-8217aa4a13c0265efd8cb81473dd7f00c68d2c34.tar.gz`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_BUNDLE_V4.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_SHA256SUMS_V4`
- `/home/codexperf/projects/gcreation-performance/.ops/ACTION_REQUIRED.md`
- `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/V4_SOURCE_VALIDATION.log`

For individual source inspection, these privileged/root/Docker-influencing files are inside the archive and hashed by V4:

- `ops/dev/install-root.sh`
- `ops/dev/install_preflight.py`
- `ops/dev/prepare_image.py`
- `ops/dev/deploy-dev.sh`
- `ops/dev/deploy_controller.py`
- `ops/dev/install-reviewed-plugin.py`
- `ops/dev/runtime.Dockerfile`
- `ops/dev/seccomp_profile.json`
- `ops/dev/gcreation-perf-dev-deploy.service`
- `ops/dev/gcreation-perf-dev-deploy.path`
- `ops/dev/gcreation-perf-dev.slice`
- `ops/dev/nginx-dev.conf.example`
- `ops/dev/trusted/gateway.mjs`
- `ops/dev/trusted/tsconfig.json`
- `packages/scanner/src/proxy.ts`
- `packages/scanner/src/proxy-main.ts`
- `packages/shared/src/security.ts`
- `packages/shared/src/auth.ts`
- `package.json`
- `package-lock.json`
- `tsconfig.json`
- `ops/dev/ROOT_TRUST_TRANSITION.md`
- `ops/dev/HUMAN_PLUGIN_ARTIFACT.md`
- `ops/dev/README.md`
- `ops/dev/BASE_IMAGE_DIGESTS.json`
- `ops/dev/review_archive.py`
- `wordpress/gcreation-performance/gcreation-performance.php`
- `wordpress/gcreation-performance/app.js`
- `wordpress/gcreation-performance/app.css`

The full manifest also hashes all other source/config/tests/docs/scripts; it is the complete immutable file list. Review all frozen dependency lock entries, not just direct dependency names.

## Exact changed-file list

Source changes from V3 handoff `02edd2da5a491ce5b882883ff4aab2a2a1e7f768` to `8217aa4a13c0265efd8cb81473dd7f00c68d2c34` (26 files):

- `.gitignore`
- `.ops/ACTION_REQUIRED.md`
- `.ops/PROJECT_STATE.md`
- `MASTER_EXEC_PLAN.md`
- `apps/audit-service/src/main.ts`
- `docs/THIRD_SECURITY_REVIEW_RESULT.md`
- `ops/dev/HUMAN_PLUGIN_ARTIFACT.md`
- `ops/dev/README.md`
- `ops/dev/ROOT_TRUST_TRANSITION.md`
- `ops/dev/deploy-dev.sh`
- `ops/dev/deploy_controller.py`
- `ops/dev/install-root.sh`
- `ops/dev/install_preflight.py`
- `ops/dev/prepare_image.py`
- `ops/dev/runtime.Dockerfile`
- `ops/dev/trusted/gateway.mjs`
- `ops/dev/trusted/tsconfig.json`
- `package.json`
- `packages/scanner/src/proxy-main.ts`
- `packages/scanner/src/proxy.ts`
- `packages/shared/src/security.ts`
- `tests/security.test.ts`
- `tests/test_deployment_kit.py`
- `tests/test_security_review_v3.py`
- `tests/test_security_review_v4.py`
- `tests/trusted-gateway.test.mjs`

Handoff-only changes (five files; three overlap the source state ledgers,28 unique changed paths overall):

- `.ops/ACTION_REQUIRED.md`
- `.ops/PROJECT_STATE.md`
- `MASTER_EXEC_PLAN.md`
- `ops/dev/SECURITY_REVIEW_BUNDLE_V4.md`
- `ops/dev/SECURITY_REVIEW_SHA256SUMS_V4`

Read-only hash verification is allowed; installation/deployment is on HOLD. Stop at this checkpoint pending the fourth human review decision.
