# Execution state

Objective: complete gCreation Website Performance Doctor MVP v0.1 on DEV only.
Version: 0.1.0. Current milestone: local implementation/security integration; DEV release gates pending.

## Preserved and completed work

- Existing history preserved: c724ac3, 6fbcc8b, 8cf5296, 55a342f. DEV probe remains intact.
- M0.1–M0.4: full authoritative specification, durable rules/docs, 31-item acceptance ledger; pushed as 212f4a6.
- M0.5: reviewable DEV kit files, root controller path defenses, locking/status/rollback, isolated non-root runtime configuration, proxy example; five unprivileged boundary tests and shell syntax checks pass. Privileged behavior remains unverified.
- M0.6–M0.12 local foundation: pinned Node/TypeScript/lockfile; Fastify health; SQLite migrations v1/v2; persistent jobs and one-running-job constraint; IP/DNS/redirect security; bounded sitemap/index discovery and page classification.
- Local code exists for M0.13–M0.30: Playwright/Lighthouse adapters, proxy/bridge, observed metrics, 16 deterministic rules, persisted events/SSE, free reports, WP gateway/UI, trusted pricing, commerce synchronization, paid reports/Fix Center, retests/comparison, expert requests/admin states, analytics and resource telemetry. Code presence is not deployed feature acceptance.

## Test evidence and scope

Pinned Node 24.21.0 clean npm ci, formatting, lint, typecheck, 16 TypeScript tests and build pass. A temporary loopback service returned HTTP 200 on 127.0.0.1:3101/health with the required structured JSON; it was then closed. This is local evidence, not deployed DEV health. Five Python deployment-boundary tests and PHP lint/commerce harness pass. UI tests use jsdom with controlled data; browser tests use injected scanner metrics. No unrelated customer site is scanned.

Verified locally: SSRF rejects unsafe URL schemes, credentials/internal hosts/private/reserved IPs and redirect-to-private destinations; HTTP/CONNECT proxy socket rejection; persistent SQLite reopen/recovery; priority and concurrency=1; actual SSE event output; trusted price boundaries; paid order uniqueness; token+order+contact authorization; fixed claims are unverified; expert request idempotency; UI escaping and token-fragment removal. Production dependency audit reported zero vulnerabilities on 2026-10-05.

## Remaining work / known limits

- Actual official-runtime Chromium sandbox and Lighthouse execution, effective cgroups, browser cleanup/egress bypass tests are not verified on DEV. Host glibc 2.28 is not the official Noble runtime; no arbitrary privileged dependencies are installed.
- Real DEV WordPress plugin activation, WooCommerce session/checkout/manual payment, report delivery and all controlled public E2E gates remain pending.
- Deployed source snapshot/build/rollback/status must be exercised after human installation; local boundary tests do not prove privilege/runtime behavior.
- Additional independent tests are needed for expert review/admin transitions, bounded resource waits, all rule fixtures, discovery edge cases, and deployment snapshot completeness.
- Privacy/log retention and actual scanner resource telemetry require deployed measurement. Raw screenshots/traces/Lighthouse JSON are not persisted by default.
- Inventory is bounded at 2001 URLs/20 sitemaps; full scope deeply scans at most eight representative pages, major scope five, free two. Truncation is disclosed; >2000 requires expert review.

## Constraints and decisions

Project-only development; original .git is read-only. Isolated metadata now lives in .ops/git-metadata; scripts/repo-git.sh preserves develop history. Host Plesk npm shebang forces Node 26; scripts/npm-dev.sh invokes npm with exact Node 24.21.0. Runtime pins: Playwright 1.63.0 and matching official Noble image, Lighthouse 13.5.0. No paid AI runtime dependency.

Audit app has only an internal Docker network; egress proxy has external bridge and internal network. Proxy pins public DNS/IPs per connection. Containers drop all capabilities, use no-new-privileges, official pinned seccomp, PID limits, read-only app mounts and bounded logs/tmpfs. App 3.5 CPU/1500 MiB + proxy 0.5 CPU/150 MiB; aggregate slice 4 CPU/1700 MiB. Browser concurrency one. DENIED_IPS must include server public addresses; controller rejects unset list.

## Deployment / Git / human actions

No privileged file has been executed. No DEV deployment request has been written. DEV still has the original WordPress baseline. Production has never been accessed or modified. Human installation/Plesk configuration is an action pending review, not a whole-project blocker.

Human action details: .ops/ACTION_REQUIRED.md and ops/dev/README.md. Human installs reviewed immutable kit, configures deny list and DEV proxy, activates plugin/page/hidden product, sets BDT/manual test payments, supplies controlled public test URL. Never request root/Plesk/Docker access for the agent.

Acceptance: REQUIREMENTS.md remains pending for deployed items. Current checks do not satisfy the complete DEV Definition of Done.
Next recommended action: finish independent tests/security fixes, commit/push this implementation milestone, then continue integration work while human installation is pending. After install: request via .ops/deploy-dev.request, inspect status/health, validate runtime constraints and controlled public customer journey, fix and redeploy until all 31 criteria are proven.
