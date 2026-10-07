# P1 checkpoint0018 — diagnostic instrumentation Stage1

**HARD_BLOCKED / P1 BLOCKED**. Stage1 source exception **PASS_REVIEW_READY**, human review REQUIRED. This is not REPAIR_3 or runtime authority.

Baseline `9c1adb0884e9f88ca8771f8ddb0f5fa0c93f8fae`; source candidate `b060ff430854046df7490875ac402d9df909b43a` (parent baseline).
Old installed hash `029c5d5714a13fbdd3565901bdc08341e36319c1ab90cf30ea6d4ab7e58c4039` is prior operator evidence; repository candidate hash `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f` is NOT INSTALLED. No fresh protected-host verification, controller installation or runtime execution occurred.

Stage1 human-authorized diagnostic source candidate b060ff430854046df7490875ac402d9df909b43a is PASS_REVIEW_READY after75 local tests and18 local static-security assessments. Only repository deploy_controller.py instrumentation and focused tests changed; installed controller remains untouched by this task and is not freshly inspected. Historical root cause remains NOT_ESTABLISHED. P1 BLOCKED / HARD_BLOCKED; full independent review PENDING; repair_cycle2, failed repair cycles2, INITIAL/REPAIR_1/REPAIR_2 consumed, retries0 and budget exhausted unchanged. P2–P7 NOT_STARTED; production/main untouched. Stage1 is source review only; installation, diagnostic runtime, deployment, Stage2 and REPAIR_3 remain unauthorized. HUMAN REVIEW REQUIRED: decide whether to accept the instrumentation candidate and separately authorize any future controller installation / diagnostic execution. No installation procedure or Stage2 authority is prepared. Evidence: .ops/reports/P1/diagnostic-instrumentation-stage1/REPORT.md.

Tests:22 focused +12 deployment +21 V3 +13 V4 +3 source-permission +4 bytecode =75 PASS on Python3.6.8. Static/security18 PASS locally; independent human acceptance REQUIRED. Journal limits:60/readiness call,2/final health,60/existing rollback;122/deploy;512 bytes/event;62464 bytes total. All non-diagnostic controller AST, V4 controls, application and image inputs unchanged.

Primary review: .ops/reports/P1/diagnostic-instrumentation-stage1/REPORT.md and REVIEW.json. Exact diff CONTROLLER.patch; authorization AUTHORIZATION.txt; package CHECKSUMS.sha256. Append-only event0018 matches LATEST_CHECKPOINT.json. Event0017 and prior evidence remain unchanged.

NO CONTROLLER INSTALLATION, RUNTIME EXECUTION, REPAIR OR DEPLOYMENT IS AUTHORIZED.
