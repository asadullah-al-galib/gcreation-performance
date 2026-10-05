# Human-reviewed DEV deployment kit

The agent must never run this installer, Docker, systemctl or Plesk administration. Review all files first. Installed controller code and its fixed Dockerfile/seccomp profile are root-owned and not writable by codexperf. The watcher accepts only `{ "action": "deploy", "commit": "<40 lowercase hex>" }`; it never sources request data or repository shell code on the host.

## Runtime pins and isolation

Node 24.21.0, Playwright package 1.63.0, official `mcr.microsoft.com/playwright:v1.63.0-noble`, Lighthouse 13.5.0. Pin decisions were verified against npm and [official Playwright Docker documentation](https://playwright.dev/docs/docker). `seccomp_profile.json` is copied verbatim from [Playwright v1.63.0](https://github.com/microsoft/playwright/blob/v1.63.0/utils/docker/seccomp_profile.json). The image includes Chromium/dependencies; project packages are installed from package-lock.json in a constrained non-root build container. The normal deploy controller never builds repository Dockerfiles.

Audit app: internal Docker network, no external route, publishes only `127.0.0.1:3101`. Validating egress proxy: internal network plus external bridge, no published ports. Browser and HTTP discovery use this proxy/bridge. Public IP validation and pinned connections reject private networks, metadata and DNS rebinding. Set DENIED_IPS to this server's public IPs and any additional local/public-internal destinations before enabling customer scans. The app cannot bypass egress using direct sockets to the internet. All public route handling uses WordPress; engine APIs require a server secret.

Each container runs uid/gid 10001, no capabilities, no-new-privileges, pinned seccomp, PID cap, local log rotation, read-only app mount and bounded tmpfs. App 3.5 CPU/1500 MiB; proxy 0.5 CPU/150 MiB. The shared `gcreation-perf-dev.slice` caps aggregate CPU at 4 and RAM at 1700 MiB. The unprivileged builder uses the same slice. No Docker group/socket is exposed to codexperf or containers. No host root/unrelated Plesk mounts. Browser sandbox remains enabled; if host kernel/seccomp cannot support it, deployment must fail rather than add SYS_ADMIN or disable sandbox.

## Manual install (human root only)

1. Review `install-root.sh`, `deploy_controller.py`, `deploy-dev.sh`, Dockerfile, seccomp and systemd files. Verify Docker engine/systemd cgroup support exists; do not grant the agent access. Confirm the fixed DEV plugin directory and real Plesk owner/group.
2. Run:

```sh
bash /home/codexperf/projects/gcreation-performance/ops/dev/install-root.sh
```

3. Edit `/etc/gcreation-perf-dev/runtime.env` as root. Keep ENGINE_SECRET private. Populate `DENIED_IPS` with the server public IPs (comma-separated). Optional `PRICING_JSON` config controls BDT prices centrally; keep all four tier boundaries at 25/100/500/2000. Resource thresholds: MIN_AVAILABLE_KB=1200000, MAX_MEMORY_PRESSURE=10. Do not use live payment secrets.
4. Add `nginx-dev.conf.example` to **DEV only** in Plesk → dev.gcreation.agency → Apache & nginx settings → Additional nginx directives. It exposes health and denies unauthenticated engine management. Future authenticated SSE proxy routes must retain the documented no-buffer settings; the current WordPress UI polls actual persisted engine events.
5. After a successful deployment, activate only the gcreation-performance plugin in the DEV WordPress admin. Create a `/performance-doctor/` page with `[gcreation_performance]`. In Performance Doctor Settings create the hidden audit product. Set DEV WooCommerce currency to BDT and configure a manual/test payment method. Disable caching for the scan/report page and plugin REST routes; cookies/nonces must remain session-specific.

## Normal agent request (unprivileged)

After all checks, commit and push to develop. Write `.ops/deploy-dev.request` atomically with the full commit hash. Do not execute installed controller code. Read `.ops/deploy-dev.status` for RUNNING/COMPLETED/FAILED and rollback result. The commit is a request label, not a source attestation: status also includes a SHA-256 digest of the immutable source snapshot. Keep the source unchanged until the watcher snapshots it.

The controller locks deployments, anchors source reads with no-follow directory descriptors, rejects symlinks/hardlinks/special files, bounds snapshot files/bytes, creates immutable source, builds/tests as non-root, starts limited runtime, checks internal and DEV health without redirects, PHP-lints the plugin, backs up and copies only the one DEV plugin, preserves Plesk ownership, rolls back failures and keeps three releases. Existing SQLite data is retained; schema changes require backward-compatible migrations for rollback.

## Validation limits

Local tests exercise path substitution and source-copy defenses, fixed runtime flags and syntax. They do **not** prove root installation, Docker/kernel sandbox compatibility, deployed egress isolation, WordPress activation, real WooCommerce checkout or effective cgroup limits. Those remain mandatory DEV release checks. No privileged files have been executed by the agent.
