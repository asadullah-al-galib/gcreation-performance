# Durable engineering rules

Authoritative scope: docs/MASTER_PRODUCT_SPEC.md. Resume from MASTER_EXEC_PLAN.md.

1. Never fabricate measurements or scan progress.
2. Never invent a plugin/root cause without supporting evidence.
3. Separate measurement from explanation; label uncertainty.
4. Deterministic rules must run without paid AI; preserve replaceable adapters.
5. Public URLs are hostile input. SSRF defense covers DNS, every redirect, browser subresources and Lighthouse.
6. Never commit credentials or log authentication secrets, cookies, payment secrets or report tokens.
7. Never touch production, main, unrelated domains or Plesk subscriptions.
8. Develop only within /home/codexperf/projects/gcreation-performance.
9. No root, escalation, Plesk admin, Docker socket/group, host security changes or privileged execution by the agent.
10. Prepare privileged DEV changes in ops/dev/ for human review/install; keep installed privileged code root-owned and immutable to codexperf.
11. Test material features, fix failures and verify observable behavior before declaring completion.
12. Prefer simple modular architecture; no speculative infrastructure or paid AI dependency.
13. Human approval is required for risky live-site changes.
14. Browser concurrency is one. Bound compute, requests, logs, artifacts, retries and cleanup.
15. Persist state, meaningful milestones and evidence. Commit/push only develop. Keep temporary state out of this file.
16. Record genuine human actions in .ops/ACTION_REQUIRED.md; continue independent work while deployment is pending.
