STATUS:
P1 HARD_BLOCKED — DIAGNOSTIC INSTRUMENTATION STAGE1 HUMAN REVIEW REQUIRED

PROCESS:
diagnostic-instrumentation-stage1

STAGE1:
APPROVED_AND_CONSUMED_FOR_SOURCE_REVIEW_ONLY / PASS_REVIEW_READY

CANDIDATE COMMIT:
b060ff430854046df7490875ac402d9df909b43a

OLD INSTALLED CONTROLLER SHA256 (PRIOR OPERATOR EVIDENCE):
029c5d5714a13fbdd3565901bdc08341e36319c1ab90cf30ea6d4ab7e58c4039

NEW REPOSITORY CANDIDATE SHA256 (NOT INSTALLED):
be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f

HUMAN ACTION:
HUMAN REVIEW REQUIRED: decide whether to accept the instrumentation candidate and separately authorize any future controller installation / diagnostic execution. No installation procedure or Stage2 authority is prepared.

REVIEW PACKAGE:
.ops/reports/P1/diagnostic-instrumentation-stage1/REPORT.md
.ops/reports/P1/diagnostic-instrumentation-stage1/REVIEW.json
.ops/reports/P1/diagnostic-instrumentation-stage1/CONTROLLER.patch
.ops/reports/P1/diagnostic-instrumentation-stage1/AUTHORIZATION.txt
.ops/reports/P1/diagnostic-instrumentation-stage1/CHECKSUMS.sha256
Candidate source/test files are pinned by the source commit and report hashes.

COUNTERS / STATE:
P1 BLOCKED; full independent review PENDING; orchestrator HARD_BLOCKED.
INITIAL failed/consumed; REPAIR_1 failed/consumed1/1; REPAIR_2 failed/consumed1/1.
repair_cycle2; failed repair cycles2; budget EXHAUSTED; automatic retries0; counters unchanged.
Root cause / failed predicate NOT_ESTABLISHED. P0 FROZEN/human PASS; P2–P7 NOT_STARTED.
Production/main untouched.

NO AUTHORITY:
Controller installation/refresh=false; diagnostic runtime execution=false; deployment=false;
REPAIR_3=false; Stage2=false; repair-budget reset/extension=false. No request or attempt consumed.
No privileged/protected-host operation, operator execution recipe, HTTP runtime probing, image/service/network action,
WordPress/Plesk/nginx change or cleanup. Existing failed runtime/evidence remains preserved.

NO CONTROLLER INSTALLATION, RUNTIME EXECUTION, REPAIR OR DEPLOYMENT IS AUTHORIZED.
