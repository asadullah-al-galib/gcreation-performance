# Second security review handoff

STATUS: READY FOR SECOND SECURITY REVIEW

Review source commit: `7887fca3a0fe6615da764b12d777efbe03d82a62` (`7887fca`).
Verification date: 2026-10-05. Workspace: `/home/codexperf/projects/gcreation-performance`.
Scope: human security review only. No installation, privileged execution or DEV deployment request is authorized at this checkpoint. Stop after the handoff. Production is out of scope.

## Checkpoint reconciliation

The initial working tree was clean, local develop and remote origin/develop were both the exact review commit, and main remained `c724ac3b50bc44d71f8620bb4ac0cccfae890de2`.
Two handoff defects existed at 7887fca: ACTION_REQUIRED.md still said PENDING REVIEW and this review bundle was absent. Only handoff metadata is corrected: ACTION_REQUIRED.md, this bundle and its SHA-256 manifest. A documentation-only follow-up commit records these artifacts; it does not change the source being reviewed. Every one of the 42 manifest files is byte-for-byte equal to its blob at 7887fca.

## Recalculated SHA-256 verification

`SECURITY_REVIEW_SHA256SUMS` covers all nine privileged/root/Docker/proxy configuration files, plus all application, package, test, WordPress and build inputs executed/copied by the controller (42 files total). It includes package.json scripts, the lockfile, TypeScript/ESLint/format configuration and scanner/egress code, not merely the Dockerfile. Hashes were calculated from current bytes and independently compared to the exact Git commit bytes; all match. `sha256sum --check` passes for all 42 files.
The manifest excludes handoff/support documentation, generated artifacts, node_modules, caches and secrets. It does not attempt to hash itself. The follow-up Git commit binds the metadata.

From the project root, verification is read-only:

```sh
sha256sum --check ops/dev/SECURITY_REVIEW_SHA256SUMS
```

Core privileged-file hashes:

| File                                      | SHA-256                                                            |
| ----------------------------------------- | ------------------------------------------------------------------ |
| ops/dev/deploy-dev.sh                     | `c2efba1043f50f11efa7c13f37c7b8cbe2141a71b09c977d8ce18561e36ac371` |
| ops/dev/deploy_controller.py              | `5038e9e3f659e8728b08aa7fddc60221966840562f91f7ada92590512a85ed75` |
| ops/dev/gcreation-perf-dev-deploy.path    | `8e39f174d037edb19df62495b55dd68fc20ea8bf563689308bd52d306d5f3f49` |
| ops/dev/gcreation-perf-dev-deploy.service | `17874a37a85ffae590293869caafec635216696ce02ff572c5bb97df0cf37291` |
| ops/dev/gcreation-perf-dev.slice          | `5e0d7042c1fc99ad74dde521ab38fc6ced81d6204abc874723453f30c3ee9a4b` |
| ops/dev/install-root.sh                   | `045b3a7cd0c6c92cb8b70825390a6f330c4844899fd06b19e3dc20afabf1d14c` |
| ops/dev/nginx-dev.conf.example            | `456defda33871f281609dd999295fc1185e19aae9d9937da25ebe6605a17b4cf` |
| ops/dev/runtime.Dockerfile                | `b410e75b5a5ea4a1c12b3dcd44260aa94a4069fd4d2d6080fef928b57b95e63e` |
| ops/dev/seccomp_profile.json              | `cc3e61cabda6bbc1e53e54d27ba4d55a9d3be829b6dd1a596f4a7b31b1cc7849` |

## Non-privileged checks rerun

- Pinned Node 24.21.0 clean install: `scripts/npm-dev.sh ci --ignore-scripts` passed.
- Format, ESLint, typecheck and build passed.
- TypeScript suite: 24 passed, zero failures.
- Deployment-kit Python suite: 11 passed, zero failures. Root identity, Docker/host commands, runtime launch, health and ownership operations are mocked in controller simulations; filesystem fixtures remain inside the project.
- PHP plugin lint and WooCommerce/session/security contract harness passed.
- `bash -n ops/dev/install-root.sh` and `sh -n ops/dev/deploy-dev.sh` passed; neither script was executed.
- Python AST parsing, seccomp JSON/default-action and systemd section checks passed. These are static checks, not installation or daemon validation. shellcheck and hadolint are unavailable and were not run.
- A fresh unprivileged source snapshot, assembled with the controller's source-copy helper and allowlist, passed clean npm ci, format:check, lint:ts, typecheck, all 24 tests and build. All host commands ran as the ordinary development user; no Docker image/container was built or started. Its dependency audit reported zero vulnerabilities.

## Human review focus and unverified behavior

Review the installer and installed immutable controller together: fixed DEV paths; trust transition; symlink/path-substitution defenses; request validation; source snapshot limits; no repository commands executed as host root by the watcher; ownership/config preservation; locking; failure cleanup; bounded releases and rollback. Review the service write paths, Docker build and runtime mounts/networks, capabilities, seccomp/sandbox, CPU/RAM/PID/log/tmpfs limits and authenticated egress bridge/proxy. The commit field labels a request; the snapshot digest records actual deployed bytes, so the label alone is not source attestation.

Actual root installation, Docker/kernel behavior, browser sandbox/cleanup, effective cgroup enforcement, SSRF egress isolation on DEV, Plesk proxy, plugin activation and WooCommerce checkout are unverified. The versioned upstream image tags are used as written in the Dockerfile; image digest and host-runtime attestations are not supplied by these local tests. Passing these checks is readiness for human review, not security approval or DEV completion. No privileged component was installed or executed, no deploy-dev.request was created, and production was not accessed or changed.

## Exact files to provide

Provide these 48 files with their repository-relative layout preserved. No runtime.env, generated config.php, report tokens, database, caches or raw customer artifacts belong in this handoff. The first 42 files are covered by the manifest; six supporting files follow.

Privileged kit and DEV proxy (nine files):

- `/home/codexperf/projects/gcreation-performance/ops/dev/deploy-dev.sh`
- `/home/codexperf/projects/gcreation-performance/ops/dev/deploy_controller.py`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev-deploy.path`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev-deploy.service`
- `/home/codexperf/projects/gcreation-performance/ops/dev/gcreation-perf-dev.slice`
- `/home/codexperf/projects/gcreation-performance/ops/dev/install-root.sh`
- `/home/codexperf/projects/gcreation-performance/ops/dev/nginx-dev.conf.example`
- `/home/codexperf/projects/gcreation-performance/ops/dev/runtime.Dockerfile`
- `/home/codexperf/projects/gcreation-performance/ops/dev/seccomp_profile.json`

Container/build/application/plugin inputs and check implementations (33 files):

- `/home/codexperf/projects/gcreation-performance/.prettierignore`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/main.ts`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/server.ts`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/store.ts`
- `/home/codexperf/projects/gcreation-performance/apps/audit-service/src/worker.ts`
- `/home/codexperf/projects/gcreation-performance/eslint.config.js`
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
- `/home/codexperf/projects/gcreation-performance/tests/advanced.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/api.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/foundation.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/scanner-lifecycle.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/security.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/test_deployment_kit.py`
- `/home/codexperf/projects/gcreation-performance/tests/ui.test.ts`
- `/home/codexperf/projects/gcreation-performance/tests/wordpress-integration.php`
- `/home/codexperf/projects/gcreation-performance/tsconfig.build.json`
- `/home/codexperf/projects/gcreation-performance/tsconfig.json`
- `/home/codexperf/projects/gcreation-performance/wordpress/gcreation-performance/app.css`
- `/home/codexperf/projects/gcreation-performance/wordpress/gcreation-performance/app.js`
- `/home/codexperf/projects/gcreation-performance/wordpress/gcreation-performance/gcreation-performance.php`

Review metadata and supporting guidance (six files):

- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_BUNDLE.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/SECURITY_REVIEW_SHA256SUMS`
- `/home/codexperf/projects/gcreation-performance/.ops/ACTION_REQUIRED.md`
- `/home/codexperf/projects/gcreation-performance/ops/dev/README.md`
- `/home/codexperf/projects/gcreation-performance/SECURITY.md`
- `/home/codexperf/projects/gcreation-performance/docs/DEV_VALIDATION_RUNBOOK.md`
