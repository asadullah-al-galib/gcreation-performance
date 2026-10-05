P0 — PROJECT GOVERNANCE FREEZE

Goal:
Re-organize the gCreation Performance Doctor MVP into one fixed execution timeline and one evidence-driven completion system.

Do NOT start P1 deployment.
Do NOT execute root, Docker, systemd, Plesk, WordPress installation, deployment requests, or production changes.
Do NOT redesign architecture unless required only to make governance documents consistent.
Do NOT modify application/runtime/security implementation in P0.

Current approved baseline:

Source commit:
8217aa4a13c0265efd8cb81473dd7f00c68d2c34

V4 handoff:
5c44cb3549aebf02ddef84d8f4a04c5f82ae7f7d

V4 STATIC SECURITY REVIEW:
PASS

Important:
This PASS is only for static security design and controlled DEV installation preparation.
DEV runtime/deployment/E2E acceptance is NOT complete.

==================================================
1. CREATE ONE AUTHORITATIVE PROJECT TIMELINE
==================================================

Create:

PROJECT_TIMELINE.md

This becomes the single authoritative execution timeline for MVP v0.1.

Organize the remaining project into exactly these Parts:

P0 — Governance Freeze
P1 — Security & DEV Deployment Foundation
P2 — Audit Engine Live Validation
P3 — WordPress Customer Flow
P4 — Paid Service Flow
P5 — Final Security / E2E / Resource Acceptance
P6 — DEV Release Candidate
P7 — First 100 Customer Validation

Do not create more top-level Parts without explicit human approval.

For every Part include:

- Purpose
- Exact scope
- Included original milestones M0.x
- Current status
- What is already implemented
- What is only locally tested
- What requires real DEV validation
- Exact entry criteria
- Exact exit criteria
- Evidence required
- Explicit non-goals
- Estimated execution time
- Dependencies
- Allowed human actions
- Allowed Codex actions
- Completion state:
  NOT_STARTED / IN_PROGRESS / BLOCKED / PASS / FROZEN

==================================================
2. MAP ALL EXISTING MILESTONES
==================================================

Map every original milestone M0.1 through M0.32 into the new Parts.

Do not delete or redefine original milestone intent.

Use these execution groups as the source structure:

M0.1–M0.4:
specification / rules / durable planning

M0.5–M0.7:
DEV kit / reproducible toolchain / health foundation

M0.8–M0.12:
SQLite / jobs / security / discovery / classification

M0.13–M0.18:
Playwright / Lighthouse / metrics / deterministic rules / SSE / free report

M0.19–M0.24:
WordPress / customer UI / site size / pricing / WooCommerce

M0.25–M0.30:
paid reports / Fix Center / retest / expert / analytics

M0.31:
security / E2E / resource acceptance

M0.32:
DEV release candidate

For every M0.x assign:

IMPLEMENTATION:
COMPLETE / PARTIAL / NOT_STARTED

LOCAL_TEST:
PASS / PARTIAL / NOT_RUN

DEV_ACCEPTANCE:
PASS / PENDING / NOT_APPLICABLE

Do not mark DEV acceptance complete based only on mocked/local tests.

==================================================
3. REBUILD THE ACCEPTANCE LEDGER
==================================================

Do not remove REQUIREMENTS.md.

Update it only if required for consistency.

Create a clear cross-map:

D01–D31
→ Part
→ original M0.x
→ existing evidence
→ remaining real DEV evidence

Keep all currently unproven deployed criteria PENDING.

No local test may be promoted to deployed acceptance.

==================================================
4. FREEZE MVP SCOPE
==================================================

Add a section:

MVP SCOPE FREEZE

Explicitly OUT OF SCOPE until first-100 validation:

- PostgreSQL migration
- Redis
- BullMQ
- Kubernetes
- paid AI/LLM runtime
- automated live optimization
- continuous monitoring platform
- production deployment
- multi-region
- horizontal scaling
- microservices split
- unnecessary dashboards
- extra customer features not already in authoritative scope

Any future Codex session must reject or defer these unless human explicitly changes MVP scope.

==================================================
5. DEFINE FIXED EXECUTION RULES
==================================================

Add these rules to PROJECT_TIMELINE.md and AGENTS.md if not already represented:

1. Work only one Part at a time.
2. Do not begin the next Part until the current Part receives human-review PASS.
3. A PASS Part becomes FROZEN.
4. Frozen Parts cannot be redesigned unless a later concrete defect proves it necessary.
5. Every Part gets maximum:
   - initial implementation/validation cycle
   - repair cycle 1
   - repair cycle 2
6. After two repair cycles, stop and report the concrete blocker instead of redesigning endlessly.
7. No speculative refactor.
8. No new infrastructure without explicit requirement.
9. Evidence is stronger than claims.
10. A blocker must contain:
    - exact failing requirement
    - exact command/test
    - exact error/evidence
    - smallest proposed remediation
11. Do not bundle unrelated improvements into a Part.
12. Never touch production.
13. Commit/push only develop.
14. Preserve all accepted V4 security boundaries.
15. Human approval is required before:
    - root execution
    - Docker privileged installation
    - systemd installation
    - Plesk/nginx modification
    - WordPress plugin installation
    - WooCommerce manual configuration that changes DEV
16. Codex must not autonomously start the next Part.
17. Timebox work to the current exit gate.
18. No “while I am here” feature additions.

==================================================
6. DEFINE PART HANDOFF FORMAT
==================================================

Every Part must end with exactly this handoff structure:

PART:
GOAL:

SOURCE COMMIT:
HANDOFF COMMIT:

CHANGED FILES:

TESTS:
- ...

REAL ENVIRONMENT EVIDENCE:
- ...

ACCEPTANCE CRITERIA:
- PASS/FAIL per criterion

UNRESOLVED:
- none
or
- exact blocker

PRODUCTION TOUCHED:
NO

CURRENT PART STATE:
PASS / BLOCKED

NEXT PART:
DO NOT START UNTIL HUMAN REVIEW

Codex must stop after this handoff.

==================================================
7. DEFINE PROJECT STATE MACHINE
==================================================

Create a simple state machine:

NOT_STARTED
→ IN_PROGRESS
→ REVIEW_READY
→ PASS
→ FROZEN

Failure path:

IN_PROGRESS
→ BLOCKED
→ REPAIR_1
→ REVIEW_READY

If still failing:

→ REPAIR_2
→ REVIEW_READY

If still failing:

→ HARD_BLOCKED
→ HUMAN DECISION

No infinite retry loop.

==================================================
8. RECORD CURRENT STATUS ACCURATELY
==================================================

Current expected status:

P0:
IN_PROGRESS during this task

P1:
NOT_STARTED
Static security prerequisite = PASS
Real installation/runtime validation = pending

P2:
NOT_STARTED
Implementation largely exists
Real browser/Lighthouse/engine DEV validation pending

P3:
NOT_STARTED
Implementation largely exists
WordPress/WooCommerce DEV acceptance pending

P4:
NOT_STARTED
Implementation largely exists
Real paid-service E2E pending

P5:
NOT_STARTED

P6:
NOT_STARTED

P7:
NOT_STARTED

Do not describe P2/P3/P4 as development-complete without differentiating:
implementation present vs real acceptance pending.

==================================================
9. UPDATE MASTER_EXEC_PLAN
==================================================

Reorganize MASTER_EXEC_PLAN.md so it becomes a concise current-state ledger.

It must point to PROJECT_TIMELINE.md as the authoritative execution order.

Remove stale statements such as:
- “next recommended action = third review”
- old review checkpoint instructions that are no longer current

Preserve historical security-review facts, but clearly label V2/V3 as historical.

Record:

V4 static security review:
PASS

Installation:
HOLD pending P1 explicit human start

==================================================
10. UPDATE ACTION_REQUIRED
==================================================

Update .ops/ACTION_REQUIRED.md to:

STATUS:
P0 GOVERNANCE REVIEW READY

It must state:

- V4 static review PASS
- privileged DEV install remains on HOLD
- next human decision is P0 governance acceptance
- P1 must not start automatically

No installation commands in ACTION_REQUIRED for P0.

==================================================
11. CREATE ONE COMPACT STATUS SUMMARY
==================================================

Create:

.ops/PROJECT_STATUS.md

Keep it very short.

Format:

PROJECT:
gCreation Performance Doctor MVP v0.1

CURRENT PART:
P0

STATE:
REVIEW_READY

STATIC SECURITY:
V4 PASS

DEV INSTALL:
NOT STARTED

PRODUCTION:
UNTOUCHED

NEXT ALLOWED ACTION:
Human review of P0 governance

NEXT FORBIDDEN ACTION:
Starting P1 automatically

SOURCE BASELINE:
8217aa4a13c0265efd8cb81473dd7f00c68d2c34

==================================================
12. VERIFY CONSISTENCY
==================================================

Before committing:

Check these files for contradictory current-next-step language:

AGENTS.md
PROJECT_TIMELINE.md
MASTER_EXEC_PLAN.md
ROADMAP.md
REQUIREMENTS.md
.ops/ACTION_REQUIRED.md
.ops/PROJECT_STATUS.md
.ops/PROJECT_STATE.md
README.md

Historical V2/V3 review documents may retain historical HOLD text.
Do not rewrite historical evidence.

Current operational docs must agree on:

- V4 static security PASS
- P0 governance review
- P1 not started
- production untouched
- no automatic next-Part execution

==================================================
13. TEST / QUALITY SCOPE FOR P0
==================================================

Because P0 is governance-only:

Do NOT rerun the entire expensive application suite unless file changes unexpectedly touch executable code.

Required checks:

- git diff --check
- markdown/content consistency review
- confirm no executable/runtime/application source changed
- confirm no privileged file changed
- confirm working tree clean after commit
- confirm pushed to origin/develop

If any executable code changes accidentally:
STOP and report it.
Do not include it in P0.

==================================================
14. COMMIT
==================================================

Commit only governance/state documentation.

Suggested commit:

docs: freeze MVP execution timeline and governance

Push to origin/develop.

==================================================
15. FINAL RESPONSE
==================================================

Return exactly:

P0 GOVERNANCE HANDOFF

SOURCE COMMIT:
<sha>

CHANGED FILES:
<list>

RUNTIME/APPLICATION CODE CHANGED:
NO

PRIVILEGED KIT CHANGED:
NO

CONSISTENCY CHECK:
PASS/FAIL

P0 EXIT CRITERIA:
- authoritative fixed timeline exists
- M0.1–M0.32 mapped
- D01–D31 mapped
- MVP scope frozen
- part state machine defined
- max two repair cycles defined
- V4 static PASS recorded
- P1 remains NOT_STARTED
- production untouched

UNRESOLVED:
none / exact blocker

CURRENT STATE:
REVIEW_READY

NEXT PART:
P1 — DO NOT START UNTIL HUMAN REVIEW

Stop.