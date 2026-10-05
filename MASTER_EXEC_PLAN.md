# Execution state

Objective: complete gCreation Website Performance Doctor MVP v0.1 on DEV only.
Version: 0.1.0. Current milestone: third-review HOLD remediations; fourth security review handoff preparation.

## Preserved and completed work

- Existing history preserved: c724ac3, 6fbcc8b, 8cf5296, 55a342f. DEV probe remains intact.
- M0.1–M0.4: full authoritative specification, durable rules/docs, 31-item acceptance ledger; pushed as 212f4a6. Implementation foundation pushed as be74524.
- M0.5: reviewable DEV kit files, root controller path defenses, locking/status/rollback, isolated non-root runtime configuration, proxy example; 33 unprivileged Python tests and shell syntax checks pass. Privileged behavior remains unverified.
- M0.6–M0.12 local foundation: pinned Node/TypeScript/lockfile; Fastify health; SQLite migrations v1/v2/v3/v4; persistent jobs and one-running-job constraint; IP/DNS/redirect security; bounded sitemap/index discovery and page classification.
- Local code exists for M0.13–M0.30: Playwright/Lighthouse adapters, proxy/bridge, observed metrics, 16 deterministic rules, persisted events/SSE, free reports, WP gateway/UI, trusted pricing, commerce synchronization, paid reports/Fix Center, retests/comparison, expert requests/admin states, analytics and resource telemetry. Code presence is not deployed feature acceptance.

## Test evidence and scope

Pinned Node 24.21.0 clean npm ci, formatting, lint, typecheck, 24 TypeScript tests and build pass. A temporary loopback service returned HTTP 200 on 127.0.0.1:3101/health with the required structured JSON; it was then closed. This is local evidence, not deployed DEV health. 33 Python deployment-boundary/security tests and PHP lint/commerce harness pass. UI tests use jsdom with controlled data; browser tests use injected scanner metrics. No unrelated customer site is scanned.

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

Current V4 candidate: app/gateway internal only; immutable trusted proxy internal plus dedicated egress network; builder offline. Proxy pins public DNS/IPs per connection. Containers drop all capabilities, use no-new-privileges, official pinned seccomp, PID limits, read-only app mounts and bounded logs/tmpfs. App3.4 CPU/1400 MiB + proxy0.5 CPU/150 MiB + gateway0.1 CPU/100 MiB; aggregate slice 4 CPU/1700 MiB. Browser concurrency one. DENIED_IPS must include server public addresses; controller rejects unset list.

## Deployment / Git / human actions

No privileged file has been executed. No DEV deployment request has been written. DEV still has the original WordPress baseline. Production has never been accessed or modified. Human installation/Plesk configuration is an action pending review, not a whole-project blocker.

Human action details: .ops/ACTION_REQUIRED.md and V4 review artifacts. Third human review is HOLD; installation, privileged execution, deployment requests and automatic PHP deployment remain unauthorized. Review the immutable image/proxy/gateway/dependency boundaries, offline artifact builder, dedicated networks, separated secrets and verified host denial. No root/Plesk/Docker authority is granted to the agent.

Acceptance: REQUIREMENTS.md remains pending for deployed items. Current checks do not satisfy the complete DEV Definition of Done.
Next action: hand off the exact V4 source/archive/hash evidence, commit/push metadata and stop at READY FOR FOURTH SECURITY REVIEW. No privileged execution or deployment request. Deployed acceptance remains pending.

## Latest refinements

Atomic persisted scan admission (5/client/hour and 50 pending jobs), trusted privacy-preserving client keys, session-bound WP CSRF nonce, DNS deadline and additional cloud-internal IP rejection, partial metric persistence, per-page pressure checks, bounded retest reuse/quota, representative page-kind coverage, observed redirect counts, per-rule detailed fix templates behind an explanation interface, focused WP admin tables/evidence, real package-selection analytics without quote inflation, and same-page secure report refresh. Retest query regression was caught by integration tests and fixed with the required sites join. No legitimate test was removed. Full dependency audit is clean after updating pinned tsx/eslint/typescript-eslint.

Latest local milestone: browser lifecycle controls covered by mocked driver tests; test-process concurrency capped at two; rollback backup preserves generated private config and ordinary file permissions plus original plugin ownership; shared backup budgets and failed-release retention are bounded. Fresh current-source nonprivileged snapshot build passed all Node gates before these final Python refinements; eleven Python helper tests pass after the refinements. No privileged controller execution or actual browser scan was used as test evidence.

Controller success and forced final-health failure are now exercised in unprivileged simulations: source digest/status, request cleanup, prior plugin/config/permissions and runtime rollback pass. Host commands, runtime launch and ownership changes are mocked; this is not installed/deployed evidence. Milestone 4af71f6 is pushed; main remains c724ac3.

## Second human security review remediation

Historical source 7887fca/handoff826a622 is HOLD (docs/SECOND_SECURITY_REVIEW_RESULT.md). Root inputs now cross a deterministic reviewed archive/data/hash/safe-extraction boundary and execute from immutable root-owned snapshots with isolated Python. Installer preflight checks ownership/hash/paths, Docker/systemd/configuration and stale triggers before changes and before enable. Auto watcher deploys only Node/browser; human-approved PHP artifact writes drop to the verified DEV PHP owner and generate config.php0600. Requests are atomically claimed, new requests survive cleanup; internal Docker network identity/configuration is verified before runtime start. Public nginx health is GET-only with no forwarded client headers/secret. Both FROM images are registry digest-pinned with recorded index/amd64 provenance. No privileged component was installed/executed. Full V3 gates and final source/handoff IDs are recorded in the V3 bundle.

Third-review candidate source 10dcabfe5642207486af7646bef489b83108fb17 is committed/pushed.33 Python and24 TypeScript tests plus full local/fresh snapshot gates pass. Exact archive hash/file lists are in ops/dev/SECURITY_REVIEW_BUNDLE_V3.md and SECURITY_REVIEW_SHA256SUMS_V3. Status READY FOR THIRD SECURITY REVIEW; HOLD still prohibits installation/execution/deployment requests. The handoff-only descendant changes metadata, not source inputs. Stop at this checkpoint; DEV acceptance remains incomplete.

## Third review HOLD / fourth-review remediation

Third review preserved accepted V3 controls and requested immutable trusted egress, offline builds, frozen dependencies, dedicated verified egress network, isolated ingress/master secret, verified self-host deny, artifact source identity and clean root interpreter startup. Local checks pass:46 Python tests (12 original,21 V3,13 V4),26 TypeScript tests and4 gateway socket tests, clean pinned npm install, formatting/lint/typecheck/application build/trusted proxy compile, PHP contract/lint and shell syntax. Exact committed source/archive validation and V4 handoff follow. No privileged component, Docker or deployment trigger has been executed. README describes current candidate; earlier ledger entries and bundles remain historical. Complete DEV acceptance remains pending. Stop after source/handoff commit and fourth review preparation.

## Fourth-review source and archive evidence

Source commit 8217aa4a13c0265efd8cb81473dd7f00c68d2c34 preserves V3 history. All46 Python/26 TypeScript/4 gateway tests pass; PHP, shell and Node gates pass. Fresh canonical archive source extraction passes offline clean install and the same gates, including trusted proxy compilation. Archive SHA256 ecef5a23ef175096cc6312ca99dc0b306ecd76dc3cd4af8aca7de94c6e0443a7;82 regular entries match committed blobs+marker; repeated export bytes identical. V4 manifest covers78 immutable files, excluding only three mutable state ledgers and the new self-referencing handoff bundle/manifest. State READY FOR FOURTH SECURITY REVIEW with HOLD. Handoff-only metadata does not change privileged/runtime inputs. Stop after push; DEV deployment is not complete.
