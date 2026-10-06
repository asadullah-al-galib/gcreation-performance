Future evidence checklist only; execution authority is PROJECT_TIMELINE.md. Current P0 governance FROZEN (human review PASS), P1 WAITING_FOR_HUMAN (execution IN_PROGRESS / independent review PENDING under P0.1); P2–P7 NOT_STARTED. V4 static security review PASS; privileged DEV installation HOLD pending separate human/operator installation/configuration. Production untouched. Sequential P1–P6 execution follows docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md; independent review remains PENDING, operator/security gates require a stop, and P7 requires separate human authorization. Do not execute this checklist during P0. Each later subsection requires its current authorized Part entry gate and human-approved action; installation recipes/review bundles alone are not permission.

# DEV acceptance runbook — pending actual runtime evidence

Use the complete 31-item ledger in REQUIREMENTS.md. Record timestamp, deployed commit/snapshot digest, command results, relevant job/order IDs (no tokens/contact secrets), measurements and limitations. A green local test is not a deployed feature claim.

## Before customer-facing testing

P1 covers separately approved human reviewed-kit/DEV nginx/deny/configuration actions. P3, after its own entry gate, covers separately approved human plugin/page/BDT/manual-payment configuration. These must not be bundled or started ahead of the ordered human Part gates. Confirm immutable root-owned deployment files; no agent Docker/root/Plesk access. Use a public test URL explicitly owned/authorized for this project with sitemap index and product-page fixtures. Never substitute an unrelated customer site. The scan policy blocks this audit server's public addresses and DEV/production hostnames, so the scan target must be a separate authorized public origin. No additional server or site is to be modified by the agent.

Human verifies effective aggregate slice and app/proxy/gateway limits, PID cap, no-new-privileges, cap drop, seccomp/browser sandbox, read-only mounts, no Docker socket, loopback-only published port and dedicated network identity/membership, immutable trusted code/image, distinct secret ownership and offline frozen-dependency builds. Share sanitized results only.

## Agent deployment / health

Only after the authorized Part explicitly permits deployment, installation is confirmed, develop is clean/pushed and a human authorizes the controlled request, prepare the deterministic committed DATA archive and verify its SHA/marker. The future atomic request contains action=deploy, full commit and archive_sha256, using the fixed source-artifacts path. P0 creates neither request nor deployment artifact. The watcher never copies arbitrary current workspace bytes. Read the specific .ops/deploy-dev.status handle until it reaches terminal state. Do not restart a live deployment because an observation timeout expired. FAILED must identify stage and rollback outcome; fix independently where possible, then commit/push and request again. A request/state file alone is not evidence of a live process.

Check internal `http://127.0.0.1:3101/health` and public `https://dev.gcreation.agency/perf-engine/health` with redirects disabled. Both must return HTTP 200 and structured development/service/version JSON. All public business/admin engine paths must return404 under the accepted health-only nginx boundary and expose no reports/customer data. Trusted localhost gateway management authentication is checked separately; browser transport uses nonce/session WordPress PHP, never the master engine secret.

## Controlled customer journey

1. Open DEV `/performance-doctor/` in a fresh browser/session. Submit the authorized controlled URL.
2. Observe persisted stages and real measured counts. Queue waiting must be explicit; no invented percentage. Confirm browser concurrency stays one when multiple jobs queue.
3. Verify sitemap/index discovery, normalized URL count, WordPress/WooCommerce clues and representative product choice. Check stored normalized metrics and issue evidence against the controlled fixture.
4. Confirm homepage browser + Lighthouse metrics, secondary-page network analysis and report rendering. Confirm all limitations/incomplete measurements are disclosed.
5. Select Major 5 / Full and Self / Expert. Check server price boundaries against inventory count; browser price tampering must fail to change the charge.
6. Use only the configured DEV manual/test payment method. Do not enter live payment secrets. Confirm order metadata, mark test payment through the human-approved DEV flow and verify exactly one paid audit despite repeated payment hooks.
7. Open the paid report link and verify token + order + checkout contact. Invalid token/order/contact must fail; IDs alone must not authorize. Keep report tokens out of URLs sent to servers, logs/screenshots and saved evidence.
8. Inspect paid Fix Center issue evidence, steps and verification. Mark Fixed must display a claim, not technical verification. Queue a previously audited page for retest; repeated pending requests reuse the job. Refresh comparisons to see real before/after measurements.
9. Request an expert and verify evidence reuse/idempotency, expert state operations and human approval for live changes. No automatic customer-site optimization is part of MVP.
10. Inspect privacy-conscious analytics: submissions/completions/failures, platforms/count, measured metrics/rules, free views, actual package selection (not price lookups), paid conversion, solution mode, expert requests, retests and scanner resource usage.

## Security and resource gates

Controlled public fixtures should include redirects to localhost/private/metadata, mixed DNS answers/rebinding scenarios where controllable, unsafe iframe/subresource/WebSocket targets and large/slow responses. All destinations must be refused. Test browser and Lighthouse egress, not just cheap fetch validation. Confirm deadlines, caps and cleanup after success, navigation error, browser crash and Lighthouse failure. Verify no Chromium processes/artifacts remain after the job. Confirm unsafe host pressure leaves WAITING_FOR_RESOURCES and bounded waits terminate visibly rather than forcing Chromium.

Human-owned runtime inspection is required for actual cgroup/network/sandbox evidence. The agent can test app-visible behavior and inspect readable status/health without obtaining additional privilege.

## Remaining release evidence

P1 runtime install/build/rollback and separately approved P3 plugin installation/rollback must be exercised within their own gates with a controlled failure, preserving prior runtime/plugin/Plesk ownership and SQLite compatibility. Verify bounded releases/logs/tmpfs and no unnecessary raw artifacts. Run all six quality commands from the pinned runtime, verify develop push, update MASTER_EXEC_PLAN and attach evidence for every D01–D31 row. Do not mark MVP complete until all rows are proven.
