# Execution state

Objective: complete gCreation Website Performance Doctor MVP v0.1 on DEV only.
Version: 0.1.0. Current milestone: local implementation/security integration; DEV release gates pending.

## Preserved and completed work

- Existing history preserved: c724ac3, 6fbcc8b, 8cf5296, 55a342f. DEV probe remains intact.
- M0.1–M0.4: full authoritative specification, durable rules/docs, 31-item acceptance ledger; pushed as 212f4a6. Implementation foundation pushed as be74524.
- M0.5: reviewable DEV kit files, root controller path defenses, locking/status/rollback, isolated non-root runtime configuration, proxy example; nine unprivileged boundary tests and shell syntax checks pass. Privileged behavior remains unverified.
- M0.6–M0.12 local foundation: pinned Node/TypeScript/lockfile; Fastify health; SQLite migrations v1/v2/v3/v4; persistent jobs and one-running-job constraint; IP/DNS/redirect security; bounded sitemap/index discovery and page classification.
- Local code exists for M0.13–M0.30: Playwright/Lighthouse adapters, proxy/bridge, observed metrics, 16 deterministic rules, persisted events/SSE, free reports, WP gateway/UI, trusted pricing, commerce synchronization, paid reports/Fix Center, retests/comparison, expert requests/admin states, analytics and resource telemetry. Code presence is not deployed feature acceptance.

## Test evidence and scope

Pinned Node 24.21.0 clean npm ci, formatting, lint, typecheck, 24 TypeScript tests and build pass. A temporary loopback service returned HTTP 200 on 127.0.0.1:3101/health with the required structured JSON; it was then closed. This is local evidence, not deployed DEV health. Nine Python deployment-boundary tests and PHP lint/commerce harness pass. UI tests use jsdom with controlled data; browser tests use injected scanner metrics. No unrelated customer site is scanned.

Verified locally: SSRF rejects unsafe URL schemes, credentials/internal hosts/private/reserved IPs and redirect-to-private destinations; HTTP/CONNECT proxy socket rejection; persistent SQLite reopen/recovery; priority and concurrency=1; actual SSE event output; trusted price boundaries; paid order uniqueness; token+order+contact authorization; fixed claims are unverified; expert request idempotency; UI escaping and token-fragment removal. Full dependency audit reports zero vulnerabilities after pinned test-tool updates on 2026-10-05.

## Remaining work / known limits

- Actual official-runtime Chromium sandbox and Lighthouse execution, effective cgroups, browser cleanup/egress bypass tests are not verified on DEV. Host glibc 2.28 is not the official Noble runtime; no arbitrary privileged dependencies are installed.
- Real DEV WordPress plugin activation, WooCommerce session/checkout/manual payment, report delivery and all controlled public E2E gates remain pending.
- Deployed source snapshot/build/rollback/status must be exercised after human installation; local boundary tests do not prove privilege/runtime behavior.
- Added local tests for all 16 rule families, bounded resource waits, expert review/admin transitions, inventory truncation and paid retest/comparison. Fresh nonprivileged deployment snapshot install/format/lint/typecheck/test/build passed. Browser/DEV E2E remains required.
- Privacy/log retention and actual scanner resource telemetry require deployed measurement. Raw screenshots/traces/Lighthouse JSON are not persisted by default.
- Inventory is bounded at 2001 URLs/20 sitemaps; full scope deeply scans at most eight representative pages, major scope five, free two. Truncation is disclosed; >2000 requires expert review.

## Constraints and decisions

Project-only development; original .git is read-only. Isolated metadata now lives in .ops/git-metadata; scripts/repo-git.sh preserves develop history. Host Plesk npm shebang forces Node 26; scripts/npm-dev.sh invokes npm with exact Node 24.21.0. Runtime pins: Playwright 1.63.0 and matching official Noble image, Lighthouse 13.5.0. No paid AI runtime dependency.

Audit app has only an internal Docker network; egress proxy has external bridge and internal network. Proxy pins public DNS/IPs per connection. Containers drop all capabilities, use no-new-privileges, official pinned seccomp, PID limits, read-only app mounts and bounded logs/tmpfs. App 3.5 CPU/1500 MiB + proxy 0.5 CPU/150 MiB; aggregate slice 4 CPU/1700 MiB. Browser concurrency one. DENIED_IPS must include server public addresses; controller rejects unset list.

## Deployment / Git / human actions

No privileged file has been executed. No DEV deployment request has been written. DEV still has the original WordPress baseline. Production has never been accessed or modified. Human installation/Plesk configuration is an action pending review, not a whole-project blocker.

Human action details: .ops/ACTION_REQUIRED.md and ops/dev/README.md. Human acknowledged the review request with “okay”; this is not installation evidence. No status/request file exists yet. Read-only checks confirm /usr/local/lib/gcreation-perf-dev and the installed watcher path unit do not exist as of the latest audit. Human installs reviewed immutable kit, configures deny list and DEV proxy, activates plugin/page/hidden product, sets BDT/manual test payments, supplies controlled public test URL. Never request root/Plesk/Docker access for the agent.

Acceptance: REQUIREMENTS.md remains pending for deployed items. Current checks do not satisfy the complete DEV Definition of Done.
Next recommended action: after human installation, use docs/DEV_VALIDATION_RUNBOOK.md to request DEV deployment and validate runtime constraints and the controlled public customer journey. Continue independent fixes revealed by review. Browser-driver mocks verify navigation-failure cleanup, sandbox/proxy flags and refusal without egress configuration; actual runtime validation is still required. Local test-process concurrency is capped at two. Inspect deployment status/health, fix and redeploy until all 31 criteria are proven.

## Latest refinements

Atomic persisted scan admission (5/client/hour and 50 pending jobs), trusted privacy-preserving client keys, session-bound WP CSRF nonce, DNS deadline and additional cloud-internal IP rejection, partial metric persistence, per-page pressure checks, bounded retest reuse/quota, representative page-kind coverage, observed redirect counts, per-rule detailed fix templates behind an explanation interface, focused WP admin tables/evidence, real package-selection analytics without quote inflation, and same-page secure report refresh. Retest query regression was caught by integration tests and fixed with the required sites join. No legitimate test was removed. Full dependency audit is clean after updating pinned tsx/eslint/typescript-eslint.

Latest local milestone: browser lifecycle controls covered by mocked driver tests; test-process concurrency capped at two; rollback backup preserves generated private config and ordinary file permissions plus original plugin ownership; shared backup budgets and failed-release retention are bounded. Fresh current-source nonprivileged snapshot build passed all Node gates before these final Python refinements; nine Python helper tests pass after the refinements. No privileged controller execution or actual browser scan was used as test evidence.
