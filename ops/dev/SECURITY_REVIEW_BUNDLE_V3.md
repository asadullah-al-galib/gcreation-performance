# Third human security review handoff

STATUS: READY FOR THIRD SECURITY REVIEW

HOLD remains in force. Review readiness is not approval. Do not install/execute privileged components or create a deployment request. Production remains out of scope. Stop at this checkpoint.

Source commit: `10dcabfe5642207486af7646bef489b83108fb17`.
Prior reviewed source/handoff: `7887fca` / `826a622` (HOLD result preserved in docs/SECOND_SECURITY_REVIEW_RESULT.md).
Handoff: a separate documentation-only descendant commit adds this V3 bundle/manifest and updates ACTION_REQUIRED/PROJECT_STATE/MASTER_EXEC_PLAN. It changes no reviewed source inputs. Its exact SHA is reported in the final handoff; avoiding a self-referential commit hash here is intentional.

## Exact review package to provide

Provide these four artifacts together. The deterministic source archive contains every source-commit file (including privileged kit, app, tests and guidance), plus REVIEW_SOURCE_COMMIT. Preserve its bytes; do not repack. All extracted files are regular data. No environment/config secret or customer artifacts are included.

- `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-10dcabfe5642207486af7646bef489b83108fb17.tar.gz`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_BUNDLE_V3.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_SHA256SUMS_V3`
- `/home/codexperf/projects/gcreation-performance/.ops/ACTION_REQUIRED.md`

Archive SHA-256: `ca59584d33530bb75020a7a3c7c2bf39c0f45ed6128f00ae062cdc681ce4df0a`.
Archive members: 74 (73 Git files plus source marker).
Manifest: 70 immutable source files, including every privileged/root/Docker-influencing input, application/test/build files and supporting immutable documents. Each hash was recalculated and compared to exact source-commit blob bytes. Mutable handoff state and the manifest/bundle themselves are excluded to avoid circular/current-state mismatch; the source archive hash still binds the original state files. The separate handoff Git commit binds current metadata.

Unprivileged verification from the project root:

```sh
sha256sum --check ops/dev/SECURITY_REVIEW_SHA256SUMS_V3
sha256sum /home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-10dcabfe5642207486af7646bef489b83108fb17.tar.gz
```

## Remediation and regression evidence

| Review finding                 | Final candidate behavior                                                                                                                                                                                                                              | Regression evidence                                                                                                                                        |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Root trust boundary            | Reviewed committed data archive, protected root copy, approved hash, bounded regular-file extraction, root-owned snapshot only; isolated Python prevents cwd/PYTHONPATH imports. Installer never returns to repository for privileged inputs.         | Installer input/order checks; root staging hash mismatch; traversal/link rejection; extracted identity; snapshot tamper; deterministic export/root refusal |
| Autonomous WordPress PHP       | Removed from controller and watcher write paths; no PHP lint/execute/deploy in auto workflow. Separate exact-commit/hash human artifact drops root before WordPress writes.                                                                           | No WP capability/paths; successful/failed runtime simulations leave WordPress untouched; drop-UID-before-write checks                                      |
| Stale triggers / request claim | Initial and pre-enable stale-trigger preflight fails, including dangling links. Fixed data schema is atomically renamed before long work; cleanup removes only claimed file.                                                                          | Stale/invalid schema tests; claim test; full running-deploy/new-request-preservation test                                                                  |
| Public engine API              | Only GET health proxied; other /perf-engine/ routes404; incoming headers/body dropped, no client engine secret forwarding. Browser → WP nonce/session REST → PHP → localhost engine + server secret.                                                  | Health-only/method/header/secret configuration checks; existing authenticated API/session tests                                                            |
| Image pins                     | Both FROM images include exact verified registry index SHA-256; linux/amd64 child manifests also verified.                                                                                                                                            | Digest/reference/provenance-record regression                                                                                                              |
| Secret permissions             | Generated WordPress config.php0600, owned by approved DEV PHP UID; no group read. Root runtime.env0600 and strict server-held secret/settings.                                                                                                        | Actual ordinary-user payload/readability/owner/mode tests; root config640 rejection; invalid secret/settings rejection                                     |
| Internal Docker network        | Create failures are fatal; exact name,64hex ID,Internal=true,bridge/local,role label and persisted ID required before container start.                                                                                                                | Configuration/identity variants; create failure; no containers started on mismatch                                                                         |
| Watcher authority              | Write access limited to runtime state and workspace .ops. No Plesk write path/plugin installer call.                                                                                                                                                  | Controller/service/installer boundaries; runtime-only deployment simulations                                                                               |
| Installer preflight            | Hash/ownership/fixed paths/no symlinks, secure settings, Docker health/systemd driver/x86_64, systemd239+ and manager required before install; repeated before enable.                                                                                | Stale preflight stops host calls; Docker/systemd capability failures; root snapshot/secret mode checks                                                     |
| Existing controls              | URL/IP/DNS pinning/redirects/proxy/sandbox/cap-drop/no-new-privileges/non-root/CPU/RAM/PID/RO mounts/log/request/artifact caps/concurrency1/runtime rollback/retention/redaction preserved. Snapshot digest has explicit filename/content boundaries. | Original app security/lifecycle suites retained; runtime flag/retention/rollback tests; digest boundary regression                                         |

## Non-privileged verification results

- Node24.21.0 clean npm ci --ignore-scripts passed; no privileged dependency setup.
- Format, ESLint, typecheck and build passed.
- 24 TypeScript tests passed; application/scanner/commerce implementations remain unchanged.
- 33 Python tests passed:12 deployment boundary/runtime simulation +21 V3 security regressions.
- PHP syntax and WooCommerce/session contract checks passed.
- Bash/sh syntax checks, all kit Python ASTs and seccomp JSON/default action passed.
- Fresh unprivileged source snapshot passed ci,format,full lint (including33 Python/PHP checks),typecheck,24 TS tests and build. Dependency audit reported zero vulnerabilities.
- Canonical Git archive exported twice to separate new files; bytes/hashes identical. Every archive member was compared with its exact source-commit blob, and all are regular files.
- V3 manifest hashes were recomputed from disk and compared independently with committed blobs; all match.
- Root identity/ownership observations, Docker/systemd/host commands, runtime launch and health are mocked in privileged-flow simulations. Data extraction and payload writes run as the actual ordinary development user under project-local fixtures. No root staging, root execution, Docker socket/group/service, Plesk operation or production access occurred.

## Exact base image references

Verified at `2026-10-05T09:24:06.962Z` by registry HTTPS, SHA-256 over raw manifest bytes compared with Docker-Content-Digest, then repeat child-manifest body/header verification. No Docker daemon was used. FROM uses immutable index digests (see [Docker FROM reference](https://docs.docker.com/reference/dockerfile/#from)).

| Image                        | Version tag           | FROM index digest                                                         | linux/amd64 manifest digest                                               |
| ---------------------------- | --------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| node                         | 24.21.0-bookworm-slim | `sha256:0e0ff40c39bc087845bfb27465a0df4ea419520094bc35842ff83dd8cbe6f9b6` | `sha256:5cbc7caba8c2c0f0bca675d1b61b9f2857e1cf1853c6164ee9dd409501a936e7` |
| mcr.microsoft.com/playwright | v1.63.0-noble         | `sha256:eff16c30e6f3f4af0a03fa4b706120d5e9b0891c344a27d64559aff5900a4a27` | `sha256:bc6ab0d6d44ff4826e4cb8c1e6d801e185bfc42bb0753f8e2a30efc70db054c7` |

Provenance endpoints:

- https://registry-1.docker.io/v2/library/node/manifests/24.21.0-bookworm-slim
- https://mcr.microsoft.com/v2/playwright/manifests/v1.63.0-noble

## Known validation limits / human review scope

Local checks do not demonstrate root installation, real Docker/kernel sandbox compatibility, actual network isolation/egress bypass resistance, effective runtime resource limits, installed service semantics, public DEV health, real FPM readability or WooCommerce E2E. Those still require separately approved later DEV validation. The human must confirm the actual DEV FPM owner; wp-config ownership alone is not proof of pool identity. ROOT_TRUST_TRANSITION.md and HUMAN_PLUGIN_ARTIFACT.md contain future review recipes with unusable placeholders, not an instruction to run them now. No root or Plesk authority is requested for the agent. The old second-review bundle is historical and not current approval.

## Exact source files changed from 826a622

26 source-change files; all original application module/plugin source files are preserved unchanged:

- `/home/codexperf/projects/gcreation-performance/.gitignore`
- `/home/codexperf/projects/gcreation-performance/.ops/ACTION_REQUIRED.md`
- `/home/codexperf/projects/gcreation-performance/.ops/PROJECT_STATE.md`
- `/home/codexperf/projects/gcreation-performance/AGENTS.md`
- `/home/codexperf/projects/gcreation-performance/ARCHITECTURE.md`
- `/home/codexperf/projects/gcreation-performance/MASTER_EXEC_PLAN.md`
- `/home/codexperf/projects/gcreation-performance/REQUIREMENTS.md`
- `/home/codexperf/projects/gcreation-performance/SECURITY.md`
- `/home/codexperf/projects/gcreation-performance/docs/DEV_VALIDATION_RUNBOOK.md`
- `/home/codexperf/projects/gcreation-performance/docs/SECOND_SECURITY_REVIEW_RESULT.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/BASE_IMAGE_DIGESTS.json`
- `/home/codexperf/projects/gcreation-performance/ops/dev/HUMAN_PLUGIN_ARTIFACT.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/README.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/ROOT_TRUST_TRANSITION.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/deploy-dev.sh`
- `/home/codexperf/projects/gcreation-performance/ops/dev/deploy_controller.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev-deploy.service`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install-reviewed-plugin.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install-root.sh`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install_preflight.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/nginx-dev.conf.example`
- `/home/codexperf/projects/gcreation-performance/ops/dev/review_archive.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/runtime.Dockerfile`
- `/home/codexperf/projects/gcreation-performance/package.json`
- `/home/codexperf/projects/gcreation-performance/tests/test_deployment_kit.py`
- `/home/codexperf/projects/gcreation-performance/tests/test_security_review_v3.py`

Handoff-only files added/updated after the source commit:

- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_BUNDLE_V3.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_SHA256SUMS_V3`
- `/home/codexperf/projects/gcreation-performance/.ops/ACTION_REQUIRED.md`
- `/home/codexperf/projects/gcreation-performance/.ops/PROJECT_STATE.md`
- `/home/codexperf/projects/gcreation-performance/MASTER_EXEC_PLAN.md`

## Exact immutable review manifest file list

- `/home/codexperf/projects/gcreation-performance/.gitignore`
- `/home/codexperf/projects/gcreation-performance/.node-version`
- `/home/codexperf/projects/gcreation-performance/.npmrc`
- `/home/codexperf/projects/gcreation-performance/.ops/.gitkeep`
- `/home/codexperf/projects/gcreation-performance/.prettierignore`
- `/home/codexperf/projects/gcreation-performance/AGENTS.md`
- `/home/codexperf/projects/gcreation-performance/ARCHITECTURE.md`
- `/home/codexperf/projects/gcreation-performance/PLANS.md`
- `/home/codexperf/projects/gcreation-performance/README.md`
- `/home/codexperf/projects/gcreation-performance/REQUIREMENTS.md`
- `/home/codexperf/projects/gcreation-performance/ROADMAP.md`
- `/home/codexperf/projects/gcreation-performance/SECURITY.md`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/main.ts`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/server.ts`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/store.ts`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/worker.ts`
- `/home/codexperf/projects/gcreation-performance/docs/DEV_VALIDATION_RUNBOOK.md`
- `/home/codexperf/projects/gcreation-performance/docs/MASTER_PRODUCT_SPEC.md`
- `/home/codexperf/projects/gcreation-performance/docs/SECOND_SECURITY_REVIEW_RESULT.md`
- `/home/codexperf/projects/gcreation-performance/eslint.config.js`
- `/home/codexperf/projects/gcreation-performance/ops/dev/BASE_IMAGE_DIGESTS.json`
- `/home/codexperf/projects/gcreation-performance/ops/dev/HUMAN_PLUGIN_ARTIFACT.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/README.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/ROOT_TRUST_TRANSITION.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_BUNDLE.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_SHA256SUMS`
- `/home/codexperf/projects/gcreation-performance/ops/dev/deploy-dev.sh`
- `/home/codexperf/projects/gcreation-performance/ops/dev/deploy_controller.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev-deploy.path`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev-deploy.service`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev.slice`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install-reviewed-plugin.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install-root.sh`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install_preflight.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/nginx-dev.conf.example`
- `/home/codexperf/projects/gcreation-performance/ops/dev/review_archive.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/runtime.Dockerfile`
- `/home/codexperf/projects/gcreation-performance/ops/dev/seccomp_profile.json`
- `/home/codexperf/projects/gcreation-performance/package-lock.json`
- `/home/codexperf/projects/gcreation-performance/package.json`
- `/home/codexperf/projects/gcreation-performance/packages/contracts/src/index.ts`
- `/home/codexperf/projects/gcreation-performance/packages/discovery/src/index.ts`
- `/home/codexperf/projects/gcreation-performance/packages/metrics/src/index.ts`
- `/home/codexperf/projects/gcreation-performance/packages/report-engine/src/index.ts`
- `/home/codexperf/projects/gcreation-performance/packages/rules/src/index.ts`
- `/home/codexperf/projects/gcreation-performance/packages/rules/src/recommendations.ts`
- `/home/codexperf/projects/gcreation-performance/packages/scanner/src/index.ts`
- `/home/codexperf/projects/gcreation-performance/packages/scanner/src/proxy-main.ts`
- `/home/codexperf/projects/gcreation-performance/packages/scanner/src/proxy.ts`
- `/home/codexperf/projects/gcreation-performance/packages/shared/src/auth.ts`
- `/home/codexperf/projects/gcreation-performance/packages/shared/src/pricing.ts`
- `/home/codexperf/projects/gcreation-performance/packages/shared/src/security.ts`
- `/home/codexperf/projects/gcreation-performance/scripts/bootstrap-toolchain.sh`
- `/home/codexperf/projects/gcreation-performance/scripts/check_dev.py`
- `/home/codexperf/projects/gcreation-performance/scripts/npm-dev.sh`
- `/home/codexperf/projects/gcreation-performance/scripts/repo-git.sh`
- `/home/codexperf/projects/gcreation-performance/tests/advanced.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/api.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/foundation.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/scanner-lifecycle.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/security.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/test_deployment_kit.py`
- `/home/codexperf/projects/gcreation-performance/tests/test_security_review_v3.py`
- `/home/codexperf/projects/gcreation-performance/tests/ui.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/wordpress-integration.php`
- `/home/codexperf/projects/gcreation-performance/tsconfig.build.json`
- `/home/codexperf/projects/gcreation-performance/tsconfig.json`
- `/home/codexperf/projects/gcreation-performance/wordpress/gcreation-performance/app.css`
- `/home/codexperf/projects/gcreation-performance/wordpress/gcreation-performance/app.js`
- `/home/codexperf/projects/gcreation-performance/wordpress/gcreation-performance/gcreation-performance.php`
