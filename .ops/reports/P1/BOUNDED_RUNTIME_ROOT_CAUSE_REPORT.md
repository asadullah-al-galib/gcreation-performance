ROOT CAUSE REPORT

EXACT FAILED LAYER:
D — gateway startup. Fresh-data and cloned-data application startup/direct health PASS in the isolated reproduction. Gateway→app path was not reached because the gateway exited.

EXACT OBSERVED ERROR:
Node.js24.21.0: Cannot find module '[REDACTED_LONG_VALUE].mjs'; MODULE_NOT_FOUND; gateway exit1. Host-published diagnostic health: connection refused.

ROOT CAUSE:
Gateway entrypoint resolution fails in the pinned immutable image. Exact mechanism remains unproven because entrypoint/argv is redacted and in-image existence/traversal metadata is absent. Missing file, wrong path and inaccessible ancestors remain distinguishable possibilities, not confirmed causes.

WHY REPAIR_1 FAILED:
Official start_runtime exhausted its readiness checks. The bounded reproduction shows a gateway process that never loads its entrypoint, preventing gateway health; this explains that failure pattern. REPAIR_1 fixed mutable source traversal and left the trusted gateway image unchanged. Confirm the diagnostic invocation matches the official entrypoint before selecting its precise correction.

WHETHER THE DEFECT IS SOURCE / CONFIG / DATA / RUNTIME / NETWORK:
Proven runtime entrypoint-resolution failure. Image packaging/source permissions versus launch-path configuration is unresolved. Application fresh/cloned startup and health work; no persisted-data or network fault is proven.

SMALLEST REMEDIATION:
Make the reviewed gateway entrypoint load at the fixed trusted location as UID/GID10001. First obtain exact gateway argv/entrypoint and pinned-image file/hash/ownership/mode/ancestor traversal evidence. No speculative change implemented.

CHANGED FILES REQUIRED:
Not yet selected. An evidenced image-packaging/permission repair would affect prepare_image.py/runtime.Dockerfile; an evidenced launch-path repair would affect deploy_controller.py. Do not change application, data, secrets or networks without a proved requirement.

V4 SECURITY BOUNDARY IMPACT:
No boundary/source change made. Changing reviewed immutable image inputs or privileged launcher requires SECURITY_REVIEW_REQUIRED before implementation. Preserve root-owned reviewed snapshots, immutable gateway/proxy, offline builds, dependency freeze, separate secrets, networks, SSRF and sandbox/resource boundaries.

REPAIR_2 TEST PLAN:
Target exact included/traversable entrypoint for UID10001 with missing/inaccessible negative cases; relevant image/archive/no-bytecode/V4 regressions; gateway socket/security regressions; exact immutable image startup/internal+host health and full P1 real DEV controls. No REPAIR_2 implementation/regression suite is claimed yet.

REPAIR_2 DEPLOYMENT REQUIREMENT:
Proven cause/minimal repair, cleared V4 disposition, targeted/relevant regressions PASS, deterministic commit/archive/image identity and oversight commit/push before one bounded request. Retries0. No mutable workspace deployment. REPAIR_2 attempts0; REPAIR_1 remains consumed1/1.

LOCAL DIAGNOSTIC:
A non-root/no-Docker fixture reproduces prepare_image source-directory0700 under umask0077 and Node MODULE_NOT_FOUND for an existing entrypoint with blocked traversal. This demonstrates why MODULE_NOT_FOUND alone cannot prove absence. Actual image permission mechanism remains unverified.

STATE:
HUMAN_CAPABILITY_GATE — exact gateway argv and pinned-image path/traversal evidence required. No retry/restart/recreation/configuration/image change or official deployment requested. Production/main untouched.
