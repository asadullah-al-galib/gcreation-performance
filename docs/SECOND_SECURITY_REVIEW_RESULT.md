SECOND HUMAN SECURITY REVIEW RESULT: HOLD

Do NOT install or execute the privileged DEV kit.

The reviewed source remains 7887fca / handoff 826a622.
Preserve all valid application work.

The human review independently verified:

- uploaded archive SHA-256;
- all 42 review-manifest hashes;
- 11 Python deployment-kit tests;
- PHP syntax;
- WooCommerce contract checks.

However the following security blockers must be remediated.

==================================================
1. ROOT TRUST BOUNDARY — CRITICAL
==================================================

install-root.sh itself is executed from the codexperf-writable repository,
and it also executes:

python3 "$SOURCE/ops/dev/deploy_controller.py" --check-install-source

as root before the controller becomes root-owned.

This is prohibited.

Redesign installation so NO executable/script/Python/module from:

/home/codexperf/projects/gcreation-performance

is ever executed as root.

Required trust transition:

reviewed Git snapshot
→ deterministic archive
→ copied as DATA into a root-only staging directory
→ root owns the copied archive
→ verify the exact human-approved SHA-256 on the root-owned copy
→ safely extract into root-owned staging
→ only then execute the installer/controller from the root-owned reviewed snapshot.

The installer itself must execute only from the root-owned reviewed snapshot.

It must never switch SOURCE back to the codexperf repository for privileged installer inputs.

Future installed controller may read the repository only as untrusted DATA
for constrained build/snapshot operations.

Document exact commands and trust transition.

==================================================
2. WORDPRESS PLUGIN AUTO-DEPLOY — CRITICAL/HIGH
==================================================

The DEV WordPress subdomain currently shares the Plesk subscription/security context.

Automatically copying arbitrary agent-controlled PHP into WordPress indirectly gives that code the authority of the Plesk PHP/site user and defeats the purpose of isolating Codex as codexperf.

For the current MVP architecture:

DISABLE autonomous WordPress plugin deployment from the root watcher.

The automated trusted watcher may deploy the constrained Node/browser audit runtime.

WordPress plugin deployment must remain a separate HUMAN-APPROVED artifact step tied to an exact reviewed commit/hash.

Do not automatically deploy arbitrary repository PHP into the Plesk site.

Design and document a human-approved plugin deployment procedure.

Future autonomous plugin deployment may be reconsidered only after DEV has a genuinely isolated Plesk subscription/system user/container.

==================================================
3. STALE REQUEST / PATH WATCHER
==================================================

Before enabling the path watcher:

- installation must FAIL if .ops/deploy-dev.request already exists;
- no existing developer-created trigger may auto-run after installation.

Controller must atomically CLAIM/RENAME a valid request before long-running work.

Do not leave deploy-dev.request present for the full deployment.

Use a fixed non-executable request schema only.

==================================================
4. PUBLIC ENGINE EXPOSURE
==================================================

The WordPress plugin already talks directly to:

http://127.0.0.1:3101

Therefore do NOT publicly reverse-proxy the entire engine API.

For MVP expose at most:

GET /perf-engine/health

through Plesk nginx.

All audit/order/report/admin/quote routes remain localhost-only and are reached server-side through the WordPress gateway.

Remove forwarding of browser-supplied:

X-Engine-Secret

from public nginx configuration.

ENGINE_SECRET must remain server-only.

Update ARCHITECTURE.md and SECURITY.md with the exact final flow:

Browser
→ WordPress nonce/session REST
→ WordPress PHP
→ localhost engine + server-held secret.

==================================================
5. PIN CONTAINER BASE IMAGES BY DIGEST
==================================================

Pin both Dockerfile FROM images by exact verified SHA-256 digest, not tag alone.

Record:

image name
version tag
digest

in SECURITY_REVIEW_BUNDLE.md.

Do not use floating/latest image references.

==================================================
6. ENGINE SECRET FILE PERMISSIONS
==================================================

Generated WordPress config.php containing ENGINE_SECRET must use:

0600

owned by the verified DEV PHP/Plesk owner unless a stricter compatible model is proven.

Do not grant unnecessary shared-group read access.

Document and test expected WordPress readability.

==================================================
7. VERIFY DOCKER NETWORK IS REALLY INTERNAL
==================================================

Do not silently ignore docker network create failure.

After create/reuse, inspect the exact network and verify:

Internal=true
expected driver/scope
expected identity

before starting APP.

Unexpected existing network configuration must fail deployment.

The app container must not receive uncontrolled external egress.

==================================================
8. REMOVE WORDPRESS WRITE ACCESS FROM AUTO WATCHER
==================================================

Because autonomous plugin deployment is now disabled,
remove automatic watcher write access to:

wp-content/plugins

from the systemd root deployment service.

The audit runtime deploy controller should not need WordPress filesystem write access.

Create a separate human-only plugin-install workflow.

==================================================
9. INSTALLER PRE-FLIGHT
==================================================

Before installing/enabling anything verify:

- root-owned reviewed snapshot/hash;
- Docker availability and daemon health;
- expected DEV paths;
- production paths are not selected;
- no unsafe symlinks;
- no stale deploy request;
- required systemd capability;
- secure runtime configuration.

Fail before enabling the watcher if any preflight check fails.

==================================================
10. PRESERVE CURRENT GOOD CONTROLS
==================================================

Do not weaken:

SSRF URL/IP protection
DNS pinning
redirect validation
validated browser egress proxy
cap-drop ALL
no-new-privileges
non-root runtime
CPU/RAM/PID ceilings
read-only source/runtime mounts
bounded logs
bounded requests/artifacts
browser concurrency=1
rollback
release retention
secret redaction
production isolation.

==================================================
11. THIRD REVIEW HANDOFF
==================================================

After remediation:

run all non-privileged quality/security tests.

Add regression tests specifically proving:

- installer never executes codexperf-writable code as root;
- root staging SHA mismatch aborts;
- stale request blocks watcher installation;
- request is atomically claimed;
- auto watcher has no WordPress write/deploy capability;
- public nginx exposes health only;
- X-Engine-Secret is not forwarded from public clients;
- Docker network mismatch fails;
- config.php secret permission requirement is 0600;
- base image references include SHA-256 digests.

Prepare:

ops/dev/SECURITY_REVIEW_BUNDLE_V3.md
ops/dev/SECURITY_REVIEW_SHA256SUMS_V3

Update:

.ops/ACTION_REQUIRED.md

to:

READY FOR THIRD SECURITY REVIEW

Do not instruct the owner to install anything.

Commit and push all fixes to origin/develop.

Report:

- new source commit SHA
- handoff commit SHA if separate
- exact files changed
- test results
- exact new review bundle list.

Stop at the third security-review checkpoint.

Production remains untouched.