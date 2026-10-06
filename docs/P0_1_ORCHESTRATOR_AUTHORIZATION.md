P0.1 — ORCHESTRATOR AUTHORIZATION + P1–P6 MASTER EXECUTION

PROJECT:
gCreation Performance Doctor MVP v0.1

CURRENT GOVERNANCE HEAD:
999ade0ea2695e92c1365a09a3e13f87bd4ef758

P0:
FROZEN — HUMAN REVIEW PASS

V4 STATIC SECURITY:
PASS

V4 IMPLEMENTATION BASELINE:
8217aa4a13c0265efd8cb81473dd7f00c68d2c34

PRODUCTION:
UNTOUCHED AND FORBIDDEN

==================================================
HUMAN AUTHORIZATION
==================================================

The human owner explicitly authorizes a bounded orchestrated execution
of Parts P1 through P6.

This is a governance amendment to the P0 rule that previously required
a new explicit human start before every Part.

The amendment is intentionally narrow:

Codex MAY automatically advance from one Part to the next within P1–P6
when the current Part's technical execution gate is fully satisfied,
all required evidence has been persisted, no human/operator action is
pending, no accepted V4 security boundary has changed, and no concrete
blocker remains.

Codex MUST NOT grant itself HUMAN REVIEW PASS or FROZEN status.

Instead, an automatically completed Part receives:

EXECUTION_STATE:
PASS

INDEPENDENT_REVIEW:
PENDING

The human/ChatGPT independent review may later convert that Part to
independently accepted/frozen status.

This umbrella authorization exists only to eliminate unnecessary manual
start prompts between safe sequential DEV validation Parts.

It does NOT authorize:

- root access by Codex
- Docker socket/group access
- systemd administration by Codex
- Plesk administration by Codex
- WordPress filesystem writes by Codex
- production access
- main branch changes
- security-boundary redesign
- live payment configuration
- arbitrary customer-site scanning
- automatic P7 execution

==================================================
0. VERIFY STARTING STATE
==================================================

Before changing anything:

1. Confirm current branch is develop.
2. Confirm origin/develop contains and currently resolves to the approved
   P0 freeze head or a direct governance-only descendant:

   999ade0ea2695e92c1365a09a3e13f87bd4ef758

3. Confirm working tree is clean.
4. Confirm P0 is recorded FROZEN / HUMAN REVIEW PASS.
5. Confirm P1 is NOT_STARTED.
6. Confirm V4 static security PASS remains recorded.
7. Confirm production/main have not been modified by this workflow.

If these assumptions are false:
STOP with exact evidence.
Do not repair history automatically.

==================================================
1. RECORD P0.1 ORCHESTRATOR AMENDMENT
==================================================

Create:

docs/P0_1_ORCHESTRATOR_AUTHORIZATION.md

Record this exact human authorization model.

Update only the minimum governance files required so they no longer
contradict orchestrated P1–P6 advancement.

Preserve:

- P0 FROZEN
- original P0 governance commit/history
- P0–P7 structure
- max two repair cycles
- V4 security freeze
- production prohibition
- human/operator privileged-action gates

The rule changes from:

"every next Part requires a new manual start"

to:

"P1–P6 have one umbrella human execution authorization, but Codex must
still stop at HUMAN_ACTION_REQUIRED, SECURITY_REVIEW_REQUIRED,
HARD_BLOCKED, or P6 final handoff."

P7 remains separately human-authorized.

Do not modify application/runtime/security implementation merely for
this governance amendment.

==================================================
2. CREATE ORCHESTRATOR STATE
==================================================

Create:

.ops/ORCHESTRATOR_STATUS.json

Use a stable machine-readable schema containing at minimum:

{
  "project": "gCreation Performance Doctor MVP v0.1",
  "mode": "P1-P6_ORCHESTRATED",
  "current_part": "P1",
  "state": "IN_PROGRESS",
  "authorization": "HUMAN_P0_1",
  "p0": "FROZEN",
  "static_security": "V4_PASS",
  "parts": {
    "P1": {
      "execution_state": "IN_PROGRESS",
      "independent_review": "PENDING",
      "repair_cycle": 0
    },
    "P2": {
      "execution_state": "NOT_STARTED",
      "independent_review": "PENDING",
      "repair_cycle": 0
    },
    "P3": {
      "execution_state": "NOT_STARTED",
      "independent_review": "PENDING",
      "repair_cycle": 0
    },
    "P4": {
      "execution_state": "NOT_STARTED",
      "independent_review": "PENDING",
      "repair_cycle": 0
    },
    "P5": {
      "execution_state": "NOT_STARTED",
      "independent_review": "PENDING",
      "repair_cycle": 0
    },
    "P6": {
      "execution_state": "NOT_STARTED",
      "independent_review": "PENDING",
      "repair_cycle": 0
    }
  },
  "human_gate": null,
  "hard_blocker": null,
  "production_touched": false
}

Maintain this file after every meaningful checkpoint.

==================================================
3. CREATE REPORT STRUCTURE
==================================================

Create:

.ops/reports/P1/
.ops/reports/P2/
.ops/reports/P3/
.ops/reports/P4/
.ops/reports/P5/
.ops/reports/P6/

Each completed Part must contain:

REPORT.md
EVIDENCE.json
CHECKSUMS.sha256

If human/operator work is required also create:

HUMAN_ACTION_REQUIRED.md

Do not store:

- ENGINE_SECRET
- APP_GATEWAY_SECRET
- FETCH_PROXY_SECRET
- cookies
- report tokens
- customer contacts
- payment credentials
- private keys

==================================================
4. EVIDENCE SCHEMA
==================================================

EVIDENCE.json must record criterion-level evidence.

Each evidence item should include:

criterion_id
part
requirement
expected
observed
result
timestamp
source_commit
deployed_archive_sha256 when applicable
deployed_snapshot_sha256 when applicable
runtime/image identity when applicable
command_or_test
exit_code when applicable
evidence_reference
limitations

Allowed result values:

PASS
FAIL
PENDING_HUMAN
NOT_APPLICABLE

Do not mark PASS from code presence alone.

Do not promote mock/local evidence into real DEV acceptance.

==================================================
5. EXECUTION STATES
==================================================

Use these orchestrator states:

IN_PROGRESS

SELF_REPAIR_1

SELF_REPAIR_2

EXECUTION_PASS

WAITING_FOR_HUMAN

SECURITY_REVIEW_REQUIRED

HARD_BLOCKED

P6_REVIEW_READY

Never invent additional retry stages.

==================================================
6. REPAIR BUDGET
==================================================

For each Part:

Initial execution cycle
+
maximum repair cycle 1
+
maximum repair cycle 2

If still failing:

HARD_BLOCKED

Stop.

Do not:
- attempt repair 3
- rewrite architecture
- hide failing tests
- weaken requirements
- change expected results
- remove valid tests
- declare success with partial evidence

A repair must address the smallest demonstrated defect.

==================================================
7. SECURITY FREEZE RULE
==================================================

The accepted V4 security architecture is frozen.

Do not autonomously change:

- root trust transition
- immutable trusted proxy/gateway boundary
- frozen dependency/image model
- network=none mutable builder
- dedicated internal/egress networks
- secret separation
- self-host deny architecture
- SSRF validation model
- human-only WordPress PHP deployment
- health-only public nginx
- seccomp/capability/non-root model
- CPU/RAM/PID boundaries
- archive identity model
- deployment request trust model

If completion appears to require modification of one of these:

set:

state = SECURITY_REVIEW_REQUIRED

document:
- exact failing criterion
- evidence
- why frozen security boundary appears involved
- smallest proposed change

STOP.

Do not implement the change automatically.

==================================================
8. HUMAN ACTION GATES
==================================================

Human actions are expected and are NOT technical failures.

When required:

set:

state = WAITING_FOR_HUMAN

Create:

.ops/reports/<PART>/HUMAN_ACTION_REQUIRED.md

The human-action file must contain only:

PURPOSE
WHY REQUIRED
EXACT REVIEWED ARTIFACT
PRECONDITIONS
MINIMUM HUMAN ACTION
SAFE COMMAND/UI STEPS
EXPECTED OUTPUT
SANITIZED EVIDENCE TO RETURN
ROLLBACK
WHAT CODEX MUST NOT DO

Prefer one bounded copy/paste human command where safely possible.

Never ask for:
- root password
- secret values
- Docker socket access for Codex
- Plesk admin credentials for Codex

After human evidence is provided or the expected safe marker/evidence
exists, resume the same Part.

Do not consume a repair cycle merely because the human gate was waiting.

==================================================
9. P1 — SECURITY & DEV DEPLOYMENT FOUNDATION
==================================================

Read the exact P1 entry/exit criteria from PROJECT_TIMELINE.md.

Goal:
prove the accepted V4 static design in real DEV.

Do NOT redesign it.

Expected areas include:

- reviewed root-owned installation transition
- approved archive/hash identity
- immutable trusted image
- frozen dependencies
- Docker/systemd runtime
- dedicated internal/egress network identity
- distinct secret placement and permissions
- offline mutable build
- constrained deployment
- internal health
- health-only public nginx
- cgroup CPU/RAM/Tasks/PID limits
- cap drop
- no-new-privileges
- seccomp
- readonly mounts
- no Docker socket
- rollback
- release retention
- stale-request behavior
- D24
- D25
- D26
- D27

P1 will necessarily contain a HUMAN_ACTION_REQUIRED checkpoint for
privileged installation/configuration.

Codex prepares and verifies everything possible first.

Stop only for the minimum human action.

After evidence is available, finish P1 automatically.

At P1 exit:

write P1 REPORT/EVIDENCE/CHECKSUMS.

If exit criteria fully pass:

P1 execution_state = EXECUTION_PASS
independent_review = PENDING

Then automatically begin P2.

==================================================
10. P2 — AUDIT ENGINE LIVE VALIDATION
==================================================

Use PROJECT_TIMELINE.md as authority.

Do not rebuild already implemented engine components unless a concrete
P2 test proves a defect.

Validate on an explicitly authorized controlled public fixture only:

- persistent SQLite/jobs
- concurrency one
- SSRF boundaries
- discovery
- sitemap
- classification
- real Playwright Chromium
- real Lighthouse
- actual normalized measurements
- 16 deterministic rule families against measured evidence
- genuine persisted progress
- SSE
- free-report API
- cleanup after failure
- resource waiting behavior

Do not scan unrelated customer sites.

Use targeted tests first.

Do not rerun the entire suite after every small change.

At P2 exit:
persist report/evidence/checksums.

If all P2 criteria pass:
advance automatically to P3.

==================================================
11. P3 — WORDPRESS CUSTOMER FLOW
==================================================

Validate:

- separately approved WordPress plugin artifact
- actual DEV activation
- config.php permission/readability
- WordPress session/nonce isolation
- customer submission
- actual persisted progress
- free report rendering
- site size/truncation
- package scope
- server-side trusted pricing
- browser price tamper rejection
- Major 5 / Full
- Self / Expert
- WooCommerce DEV cart/session
- BDT/manual test checkout
- correct order metadata
- no browser master secret

Autonomous watcher MUST NOT deploy PHP.

P3 therefore contains a HUMAN_ACTION_REQUIRED gate for the reviewed
WordPress plugin and any required DEV WooCommerce manual configuration.

Prepare the smallest reviewed artifact and exact human procedure.

Wait.

After evidence exists, continue P3 automatically.

At successful exit:
persist report/evidence/checksums
then automatically start P4.

==================================================
12. P4 — PAID SERVICE FLOW
==================================================

Validate real controlled DEV flow:

- paid audit job
- repeated payment hook idempotency
- secure paid-report access
- invalid authorization rejection
- Fix Center
- evidence/fix-step integrity
- mark-fixed remains a claim
- retest restricted to audited pages
- idempotent pending retest
- measured before/after
- expert request
- admin state control
- evidence reuse
- real labeled analytics events
- measured resource records

Use manual/test DEV payment only.

No live payment secrets.

Persist P4 report/evidence/checksums.

If all gates pass:
automatically start P5.

==================================================
13. P5 — FINAL SECURITY / E2E / RESOURCE ACCEPTANCE
==================================================

This is the comprehensive validation Part.

Do not use P5 to redesign the product.

Re-run the complete relevant automated suite against the exact candidate.

Perform controlled real DEV validation for D01–D29.

Cover:

- full free journey
- checkout/test payment
- paid audit
- report
- Fix Center
- retest
- expert
- analytics
- SSRF
- redirect/subresource restrictions
- browser/Lighthouse egress
- concurrency
- timeout/error/crash cleanup
- resource pressure
- cgroups
- PIDs
- logs/artifacts
- network isolation
- secret boundaries
- rollback evidence
- production untouched

If some effective host/runtime evidence requires a privileged human
inspection, create one consolidated P5 HUMAN_ACTION_REQUIRED instead
of many fragmented requests.

After successful P5:
persist report/evidence/checksums
and automatically start P6.

==================================================
14. P6 — DEV RELEASE CANDIDATE
==================================================

Do not add features.

Bind the exact accepted DEV candidate:

- source commit
- source archive SHA
- snapshot SHA
- trusted image identity
- plugin artifact identity
- deployed runtime identity
- P1–P5 evidence
- D01–D31 ledger
- rollback compatibility
- develop branch state
- production/main untouched

Reconcile REQUIREMENTS.md.

D30 and D31 must receive real final evidence.

Create:

.ops/reports/P6/REPORT.md
.ops/reports/P6/EVIDENCE.json
.ops/reports/P6/CHECKSUMS.sha256

Also create:

.ops/FINAL_AUDIT_INDEX.md

This index must link every:
P1 report
P2 report
P3 report
P4 report
P5 report
P6 report
D01–D31 criterion
source/deployment identity
known limitation
human evidence item

Set:

current_part = P6
state = P6_REVIEW_READY

STOP.

Do NOT start P7.

Do NOT claim production readiness.

Do NOT merge main.

==================================================
15. REPORT QUALITY RULE
==================================================

Reports must distinguish:

IMPLEMENTED

LOCAL_TESTED

REAL_DEV_VERIFIED

HUMAN_ATTESTED

NOT_VERIFIED

Never collapse these into one generic PASS.

A Part's EXECUTION_PASS means its defined technical exit evidence is
present.

It does not mean independent human/ChatGPT audit has approved it.

==================================================
16. GIT CHECKPOINTING
==================================================

Use develop only.

Commit meaningful checkpoints.

At minimum commit:

- P0.1 authorization/orchestrator setup
- each Part execution report
- each actual repair
- P6 final handoff

Do not create noisy commits for transient logs.

Push each meaningful checkpoint to origin/develop.

This Git repository is the communication bridge with independent review.

==================================================
17. CODEX CAPACITY / TIME DISCIPLINE
==================================================

Avoid wasting context and compute.

At each resume:

read only:

PROJECT_TIMELINE.md
AGENTS.md
MASTER_EXEC_PLAN.md
.ops/PROJECT_STATUS.md
.ops/ORCHESTRATOR_STATUS.json
current Part report/evidence files

Do not repeatedly reread/rewrite the entire project history unless a
specific defect requires it.

Use:

targeted test
→ focused repair
→ targeted regression

Run the comprehensive suite mainly at:
- material boundary changes
- P5
- P6

Do not perform repeated full security re-audits of unchanged V4 frozen
components.

Do not duplicate old evidence files.

Reference immutable prior evidence by commit/hash.

Prefer persisted compact evidence over verbose chat output.

==================================================
18. PRODUCTION SAFETY
==================================================

At every Part transition verify:

production_touched = false

Forbidden:

- production.gcreation.agency or equivalent production config
- production WordPress writes
- production database operations
- main branch modification/merge
- live payment credentials
- customer-site changes
- unrelated domains

Any accidental production contact:

STOP IMMEDIATELY
record exact evidence
state = HARD_BLOCKED

==================================================
19. FINAL CODEX CHAT BEHAVIOR
==================================================

Do not flood chat with step-by-step narrative.

Continue independently while safe.

Only interrupt the human for:

1. WAITING_FOR_HUMAN
2. SECURITY_REVIEW_REQUIRED
3. HARD_BLOCKED
4. P6_REVIEW_READY

For a human gate return:

ORCHESTRATOR HUMAN GATE

PART:
STATE:
PURPOSE:
ACTION FILE:
CURRENT COMMIT:
WHAT HUMAN MUST DO:
WHAT CODEX WILL DO AFTER:
PRODUCTION TOUCHED:
NO

For final completion return:

P1–P6 ORCHESTRATOR HANDOFF

CURRENT STATE:
P6_REVIEW_READY

P1:
EXECUTION_PASS / other

P2:
EXECUTION_PASS / other

P3:
EXECUTION_PASS / other

P4:
EXECUTION_PASS / other

P5:
EXECUTION_PASS / other

P6:
EXECUTION_PASS / other

FINAL AUDIT INDEX:
.ops/FINAL_AUDIT_INDEX.md

FINAL COMMIT:
<sha>

UNRESOLVED:
<none or exact issues>

PRODUCTION TOUCHED:
NO

INDEPENDENT REVIEW:
PENDING

P7:
NOT_STARTED — REQUIRES SEPARATE HUMAN AUTHORIZATION

Stop.