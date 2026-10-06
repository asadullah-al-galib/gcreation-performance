# Durable engineering rules

Authoritative product scope: docs/MASTER_PRODUCT_SPEC.md. Authoritative execution order and gates: PROJECT_TIMELINE.md. Resume from the concise MASTER_EXEC_PLAN.md and .ops/PROJECT_STATUS.md. The human P0 governance request in docs/P0_GOVERNANCE_FREEZE_REQUEST.md supersedes older automatic-continuation instructions; docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md narrowly amends sequential execution for P1–P6. Resume also from .ops/ORCHESTRATOR_STATUS.json and current Part evidence. Current human Master Authorization V2 is docs/P0_2_AUTONOMOUS_AUTHORIZATION.md; it supersedes routine DEV micro-approvals, not V4/privilege boundaries.

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
16. Record genuine human actions in .ops/ACTION_REQUIRED.md; independent work may continue only inside the current authorized Part while deployment is pending. A pending human gate never authorizes the next Part.

17. No repository executable/module may run as root. Privileged installer inputs must be the human-approved archive verified and extracted into a root-only reviewed snapshot.
18. The automated watcher deploys only the constrained audit runtime. WordPress PHP deployment requires a separate human-approved commit/hash artifact; it is never an autonomous watcher operation.
19. Public nginx exposes only engine health. Business/admin engine routes stay localhost-only; ENGINE_SECRET stays server-side.

The human-approved V4 source 8217aa4a13c0265efd8cb81473dd7f00c68d2c34/handoff 5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d has static security review PASS only. It does not grant installation/runtime/E2E acceptance. P0 remains FROZEN with human PASS. P0.2 authorizes bounded P1–P6 DEV execution through approved constrained capabilities. The exact reviewed controller refresh is approved, but raw root/escalation/general privilege remains forbidden; absent capability is HUMAN_CAPABILITY_GATE. Current review status lives in PROJECT_TIMELINE.md and .ops/PROJECT_STATUS.md, not in archived installation recipes.

## Fixed execution governance

20. Work only one Part at a time, in the fixed P0–P7 order in PROJECT_TIMELINE.md. Do not add top-level Parts without explicit human approval.
21. P0.2 grants bounded sequential P1–P6 DEV execution. Advance after required real technical exits through approved constrained interfaces, preserving V4 and repair limits. Routine micro-approvals/external oversight PENDING do not block; never fabricate independent PASS/FROZEN. Stop only at the seven P0.2§34 conditions; P6_REVIEW_READY stops for UAT; P7/production are not authorized.
22. Frozen Parts cannot be redesigned unless a later concrete defect proves a narrowly scoped repair necessary. Record the failing requirement and affected frozen baseline before repair; preserve accepted V4 security boundaries.
23. Each Part has at most one initial implementation/validation cycle, repair cycle 1 and repair cycle 2. After two failed repair cycles stop, record HARD_BLOCKED and seek a human decision. No infinite retries or speculative redesign.
24. A blocker identifies exact failing requirement/command/error/evidence/smallest remediation. Missing an approved launch-critical capability is HUMAN_CAPABILITY_GATE per P0.2§7, not a request to repeat granted approval. Human waiting spends no repair; existing failures/counters/evidence remain intact.
25. No speculative refactor, unrelated improvements, new infrastructure without an explicit requirement, or “while I am here” features. Timebox work to the current exit gate.
26. Evidence is stronger than claims. Separate implementation, local tests and real DEV acceptance. Only independent review grants human PASS/FROZEN. EXECUTION_PASS requires all technical exit evidence; local/mock tests cannot grant deployed acceptance.
27. Use only already approved constrained DEV interfaces under P0.2; authority never grants agent raw root/escalation/Docker socket/group/Plesk-admin. The exact REPAIR_1 controller refresh is approved subject to all existing trust/rollback checks; if capability is absent, a designated human operator must perform it. Frozen-boundary changes/unavailable capabilities follow explicit P0.2 stop conditions. No self-created general privileged bridge.
28. Persist meaningful process/Part evidence/checksums and push develop. Maintain append-only .ops/oversight/events/ plus LATEST_CHECKPOINT.json/.md per P0.2. Continue safe ordered P1–P6 after technical exits unless a defined stop applies; external oversight PENDING is non-blocking. Never claim external approval without recorded decision. P0 stays FROZEN; production/main/P7 forbidden.
29. Enforce MVP SCOPE FREEZE until first-100 validation. Reject/defer PostgreSQL, Redis, BullMQ, Kubernetes, paid AI/LLM runtime, automated live optimization, a continuous monitoring platform, production deployment, multi-region, horizontal scaling, a microservices split, unnecessary dashboards and customer features outside authoritative scope unless the human explicitly changes scope. First-100 data alone does not authorize a scope change.
30. Preserve the approved V4 immutable proxy/gateway/image, offline builds, frozen dependency baseline, dedicated verified networks, distinct secrets, verified self-host deny, archive identity, reviewed root snapshot, human-only PHP and health-only nginx boundaries. Governance changes do not authorize implementation changes.
