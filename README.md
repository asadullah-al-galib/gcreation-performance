# gCreation Performance Doctor

Website and WordPress performance diagnosis MVP v0.1. DEV: https://dev.gcreation.agency. Production is out of scope.

Start with [MASTER_EXEC_PLAN.md](MASTER_EXEC_PLAN.md), [complete specification](docs/MASTER_PRODUCT_SPEC.md), [acceptance ledger](REQUIREMENTS.md) and [security contract](SECURITY.md). Existing DEV availability probe remains in scripts/check_dev.py.

## Local development

All development stays in this repository. Host Node 26/Plesk npm is not the validated runtime. Bootstrap the exact project-local Node 24.21.0, then use the wrapper:

```sh
scripts/bootstrap-toolchain.sh
scripts/npm-dev.sh ci
scripts/npm-dev.sh run format:check
scripts/npm-dev.sh run lint
scripts/npm-dev.sh run typecheck
scripts/npm-dev.sh test
scripts/npm-dev.sh run build
```

These expose the required standard npm scripts. On an already pinned Node environment, plain npm commands work. npm caches, local SQLite and test artifacts remain under ignored .ops directories. Do not run Chromium on this shared host outside the reviewed isolated runtime.

The engine binds loopback port 3101 and requires a strong ENGINE_SECRET for all routes except health. Real scan execution additionally requires the validating proxy/HTTP bridge and isolated browser network. Tests inject controlled measurements; they never scan unrelated customer websites. Browser/Lighthouse and actual WordPress/WooCommerce DEV behavior still require runtime validation.

## Git and deployment

The original .git is read-only. `scripts/repo-git.sh` uses isolated metadata in `.ops/git-metadata` with the complete remote develop history. It does not reset the original repository. Never modify main.

The [DEV kit](ops/dev/README.md) is for human review and root installation only. The agent never runs privileged files or Docker. [Human actions](.ops/ACTION_REQUIRED.md) cover installation, DEV proxy, WordPress setup and a controlled public fixture target. Independent development continues while those actions are pending.
