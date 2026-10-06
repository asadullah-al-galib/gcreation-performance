# Working plan rules

[PROJECT_TIMELINE.md](PROJECT_TIMELINE.md) is the only authoritative execution order. MASTER_EXEC_PLAN.md is the concise state/cycle ledger and REQUIREMENTS.md is the evidence cross-map. Product scope remains docs/MASTER_PRODUCT_SPEC.md, with the later P0 governance request overriding old automatic-continuation instructions.

Current gate: P0 governance FROZEN, human review PASS. V4 static security review PASS; Repair source security review PASS (source only); P1 WAITING_FOR_HUMAN (execution IN_PROGRESS / independent review PENDING under P0.1); P2–P7 NOT_STARTED. Privileged DEV installation HOLD pending separate human fresh-stage recovery/installation approval. Production untouched. Sequential P1–P6 execution follows docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md; independent review remains PENDING, operator/security gates require a stop, and P7 requires separate human authorization.

Within the one authorized Part: inspect → reconcile → implement/validate only its scope → document exact evidence → commit/push develop → persist report/evidence/checksums → gated P0.1 transition or stop. Independent review PASS freezes a Part. Sequential P1–P6 technical execution instead follows P0.1; P7 needs separate explicit human instruction. Each Part has an initial cycle and at most two repairs; failed repair 2 becomes HARD_BLOCKED/human decision, not a speculative redesign.

Preserve accepted history and V4 boundaries. Original .git is read-only; use project-local .ops/git-metadata through scripts/repo-git.sh. No development outside the authorized project. No unrelated improvements or infrastructure, no privileged agent actions, and no production changes. Independent work while awaiting an action is limited to the current Part; a pending gate never authorizes continuing into another Part.

P0 performs documentation/diff/content/unchanged-code/Git checks only. Do not execute the entire application suite unless an executable change occurred; if one occurred accidentally, stop/report it and exclude it from P0.
