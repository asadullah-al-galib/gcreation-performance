THIRD HUMAN SECURITY REVIEW RESULT: HOLD

Do NOT install or execute the privileged DEV kit.

The third review independently verified:

- archive SHA-256 matches;
- 70/70 V3 manifest hashes match;
- archive paths/types are safe;
- root-owned reviewed archive transition is acceptable;
- autonomous WordPress PHP deployment is correctly removed;
- health-only nginx design is correct;
- base image digest pins match current official registry metadata.

Preserve all previously accepted controls.

The remaining blockers are specifically the trust/network boundary for mutable
agent-controlled runtime/build code.

==================================================
1. TRUSTED EGRESS ENFORCEMENT — CRITICAL
==================================================

The current scanner/fetch security proxy is built from mutable application source:

packages/scanner/src/proxy.ts
packages/scanner/src/proxy-main.ts

and future autonomous deployments can replace that code.

That proxy is therefore NOT an acceptable external security enforcement boundary.

Redesign so private/self-host/metadata egress enforcement is implemented by a
HUMAN-REVIEWED, ROOT-INSTALLED, IMMUTABLE trusted component.

Acceptable patterns include:

A. Bake the reviewed proxy implementation into the root-installed trusted runtime
image and NEVER mount release output into the trusted proxy container;

or

B. use another fixed trusted proxy implementation/configuration whose policy is
root-owned and immutable to codexperf.

The mutable application container may talk through the trusted proxy.

It must not be able to replace or modify the trusted egress policy.

Future changes to trusted proxy/security-policy code require a new human security review.

==================================================
2. NO DEFAULT DOCKER BRIDGE FOR UNTRUSTED CODE — CRITICAL
==================================================

Do not run agent-controlled builder/test scripts with:

--network=bridge

Untrusted repository scripts must not receive direct host/private/public Docker
network connectivity.

For MVP prefer:

- trusted dependencies frozen/pinned during reviewed root image installation;
- future mutable source builds/tests run with --network=none.

If dependency download is required during a future build, it must use a separately
trusted restricted egress mechanism.

Do not allow npm/package scripts direct Docker bridge access.

==================================================
3. FREEZE DEPENDENCIES FOR MVP
==================================================

For the first-100-site MVP, freeze:

package.json
package-lock.json
runtime dependency set

to the human-reviewed dependency baseline.

Build the reviewed dependencies into the trusted build/runtime image during the
reviewed root installation.

Autonomous source deployment must fail if dependency manifests differ from the
approved hashes.

Dependency updates require a new reviewed image/security handoff.

This allows application:

format
lint
typecheck
test
build

to execute with:

--network=none

during autonomous deployments.

==================================================
4. DEDICATED EGRESS DOCKER NETWORK
==================================================

Do not connect the trusted proxy to Docker's shared default "bridge".

Create and verify a dedicated network such as:

gcreation-perf-dev-egress

Only the trusted proxy may attach to this egress network.

Mutable application:
internal network only.

Trusted proxy:
internal network + dedicated egress network.

No unrelated container should be attached.

Verify network:

exact name
exact persisted ID
driver=bridge
scope=local
expected labels
expected Internal value

and fail closed on mismatch.

The internal network remains Internal=true.

==================================================
5. ENGINE SECRET SEPARATION
==================================================

Do not provide ENGINE_SECRET to an externally-egress-capable proxy unless absolutely
necessary.

Prefer this trust model:

Browser
→ WordPress nonce/session REST
→ WordPress PHP
→ trusted localhost auth/gateway
→ mutable audit application on internal network.

The trusted ingress component holds ENGINE_SECRET.

The mutable application should not need the WordPress master engine secret if the
trusted gateway can authenticate/forward requests safely.

For app ↔ trusted fetch proxy authentication, use a separate narrowly scoped
FETCH_PROXY_SECRET if authentication is needed.

Never reuse ENGINE_SECRET as the public-egress proxy credential.

Document exact secret ownership and which process/container receives each secret.

==================================================
6. SELF-HOST DENY MUST BE VERIFIED
==================================================

Preflight must not merely check that DENIED_IPS contains globally-routable IPs.

It must verify that the current DEV host/server public addresses are actually denied.

At minimum, for this environment, ensure the server IP:

103.112.63.86

cannot be scanned by raw IP.

Prefer resolving the approved DEV hostname(s) during human preflight and requiring
every resolved public address to be present in the root-owned deny configuration.

Application/proxy validation must continue blocking:

dev.gcreation.agency
performance.gcreation.agency
localhost/private/link-local/metadata ranges
raw server public IPs.

==================================================
7. DEPLOYMENT SOURCE IDENTITY
==================================================

Do not represent the 40-hex request field as an attested Git commit while deploying
arbitrary current-workspace bytes.

Either:

A. bind each deployment to an immutable deterministic source artifact:
   commit + archive SHA-256 + commit marker,

or

B. rename the field to request/source label and make snapshot_sha256 the canonical
deployed identity.

Prefer deterministic per-deployment source artifacts so build input cannot change
mid-copy and deployment evidence is reproducible.

Never execute source artifacts on the root host.

They remain untrusted DATA and execute only inside the constrained build/runtime
environment.

==================================================
8. CLEAN ROOT EXECUTION ENVIRONMENT
==================================================

Harden the documented future root installer invocation using a clean environment,
for example an equivalent of:

env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin ...

so BASH_ENV/PYTHON/environment inheritance cannot affect the reviewed installer
transition.

Do not weaken Python -I isolation.

==================================================
9. PRESERVE EVERYTHING ALREADY ACCEPTED
==================================================

Do not regress:

reviewed root snapshot/hash transition
safe archive extraction
WordPress human-only deployment
0600 plugin secret
health-only public nginx
no browser engine-secret forwarding
atomic request claim
stale-request fail closed
digest-pinned images
non-root runtime
cap-drop ALL
no-new-privileges
seccomp
CPU/RAM/PID ceilings
read-only source/runtime mounts
bounded logs/artifacts
concurrency=1
SSRF URL/DNS/redirect validation
rollback
production isolation.

==================================================
10. REGRESSION TESTS
==================================================

Add tests proving:

- mutable release output cannot replace the trusted egress proxy;
- trusted proxy container does not mount release output as executable proxy code;
- builder runs with no direct network;
- autonomous dependency-manifest changes are rejected;
- default Docker bridge is not used by APP, trusted proxy or builder;
- dedicated egress network identity/configuration is verified;
- proxy does not receive ENGINE_SECRET if final design separates secrets;
- raw 103.112.63.86 is denied;
- required self-host IPs missing from DENIED_IPS fail preflight;
- deployment source identity/hash behavior matches documented semantics;
- all prior V3 regressions continue passing.

==================================================
11. FOURTH SECURITY REVIEW HANDOFF
==================================================

After remediation:

run all non-privileged tests and quality gates.

Prepare:

ops/dev/SECURITY_REVIEW_BUNDLE_V4.md
ops/dev/SECURITY_REVIEW_SHA256SUMS_V4

Update:

.ops/ACTION_REQUIRED.md

to:

READY FOR FOURTH SECURITY REVIEW

Do NOT instruct the owner to install yet.

Provide:

- exact new source commit;
- handoff commit;
- deterministic source archive;
- archive SHA-256;
- V4 review bundle;
- V4 manifest;
- ACTION_REQUIRED;
- exact changed-file list;
- complete test results.

Stop at the fourth security-review checkpoint.

Production remains untouched.