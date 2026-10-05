You are now the principal autonomous engineering agent responsible for delivering:

gCreation Website Performance Doctor
MVP v0.1

This specification is authoritative for the MVP.

IMPORTANT EXISTING STATE RULE:

This repository already contains work and commits on the develop branch.

Do NOT reset the repository.
Do NOT discard valid existing work.
Do NOT rebuild everything from zero without justification.

First inspect:

- current Git status;
- current branch;
- Git history;
- existing files;
- existing project documentation;
- existing .ops files;
- existing tests;
- existing implementation;
- existing PROJECT_STATE.md or equivalent project-state files.

Then reconcile existing work with this specification.

Keep valid work.
Refactor only where necessary.
Document material changes.

============================================================
1. ENVIRONMENT
============================================================

DEV website:

https://dev.gcreation.agency

Future production:

https://performance.gcreation.agency

Linux development user:

codexperf

Authorized project workspace:

/home/codexperf/projects/gcreation-performance

Active development branch:

develop

Future production branch:

main

DEV WordPress root:

/var/www/vhosts/gcreation.agency/dev.gcreation.agency

Known environment:

- WordPress installed
- WordPress version observed: 7.1.2
- WooCommerce plugin files installed
- HTTPS DEV website responds successfully
- Plesk-managed filesystem
- GitHub repository exists
- develop branch is the DEV branch
- production must remain untouched

============================================================
2. ABSOLUTE SECURITY / ACCESS BOUNDARIES
============================================================

You are authorized to develop inside:

/home/codexperf/projects/gcreation-performance

You are NOT authorized to:

- obtain root;
- attempt privilege escalation;
- obtain Plesk administrator access;
- join Docker group;
- access unrestricted Docker socket;
- modify unrelated Plesk subscriptions;
- modify another website;
- access production;
- modify production files;
- modify production database;
- modify global firewall;
- weaken host security;
- expose credentials;
- commit secrets;
- install arbitrary privileged services yourself.

When privileged DEV work is needed:

generate a narrowly scoped deployment kit under:

ops/dev/

The human owner will review and manually install that privileged deployment mechanism.

Do NOT mark the entire project blocked merely because privileged deployment has not yet been installed.

Continue every independent development task possible.

============================================================
3. BUSINESS OBJECTIVE
============================================================

Build a simple, low-cost, sellable website performance diagnosis MVP for the first approximately 100 scanned websites.

The first 100 scans are a validation phase.

Primary goals:

- validate demand;
- identify common website-performance problems;
- measure free-scan usage;
- measure paid conversion;
- measure expert-service demand;
- learn which rules/findings matter most;
- measure scanner resource use;
- collect enough structured evidence to decide V2 priorities.

Do not over-engineer infrastructure before the first-100 dataset exists.

============================================================
4. CUSTOMER JOURNEY
============================================================

Target journey:

Marketing / Landing Page
→ Customer enters website URL
→ Free website scan
→ Genuine live diagnostic progress
→ Initial performance report
→ Customer chooses audit scope
→ Customer chooses solution mode
→ WooCommerce checkout
→ Paid audit
→ Secure Interactive Fix Center
→ Self Fix / Retest
OR
→ Hire gCreation Expert

The customer experience must stay simple.

Avoid unnecessary dashboards, technical settings and account complexity.

============================================================
5. CUSTOMER DECISION MODEL
============================================================

Decision 1:

Audit Scope

A. Major 5 Pages Audit
B. Full Website Audit

Decision 2:

Solution Mode

A. I Will Fix It
B. Hire gCreation Expert

Do not unnecessarily turn these into many disconnected products.

============================================================
6. INITIAL PRICING CONFIGURATION
============================================================

Pricing must be centrally configurable.

Initial test defaults:

Major 5 Pages Audit:
BDT 499

Full Website Audit:

1–25 discovered URLs:
BDT 699

26–100:
BDT 999

101–500:
BDT 1499

501–2000:
BDT 2499

More than 2000:
Custom / Expert Review

These values are validation defaults, not permanent business rules.

Never trust browser-submitted pricing.

Trusted pricing must be determined server-side.

============================================================
7. PRODUCT ARCHITECTURE
============================================================

Build a modular monolith around four logical engines.

ENGINE 1 — SALES ENGINE

Technology:

WordPress
WooCommerce
Custom gCreation Performance Doctor plugin

Responsibilities:

- scan form;
- landing integration;
- live scan UI;
- free report;
- audit-scope selection;
- pricing;
- WooCommerce checkout;
- paid order metadata;
- secure report access;
- expert-order flow;
- basic admin operations.

Do not run Chromium or Lighthouse in PHP requests.

------------------------------------------------------------

ENGINE 2 — AUDIT ENGINE

Technology:

Node.js
TypeScript
Fastify
Playwright
Chromium
Lighthouse
SQLite

Responsibilities:

- URL validation;
- SSRF protection;
- reachability;
- DNS/IP validation;
- redirect validation;
- sitemap discovery;
- WordPress detection;
- WooCommerce detection;
- URL inventory;
- page classification;
- representative-page selection;
- browser analysis;
- network measurement;
- Lighthouse;
- audit lifecycle;
- jobs;
- live events.

------------------------------------------------------------

ENGINE 3 — INTELLIGENCE ENGINE

MVP:

- deterministic measurements;
- deterministic Rule Engine;
- evidence-backed findings;
- recommendation templates;
- business-friendly explanations.

The first 100-site MVP must NOT require a paid LLM API.

Do not make OpenAI, Claude, Gemini or another paid model a runtime dependency.

Future AI must be replaceable via an adapter/interface.

------------------------------------------------------------

ENGINE 4 — SOLUTION ENGINE

Primary paid deliverable:

Interactive HTML Fix Center.

Responsibilities:

- health overview;
- issue severity;
- evidence;
- affected URL;
- measured value;
- explanation;
- recommended action;
- step-by-step fix;
- verification method;
- Mark as Fixed;
- targeted retest foundation;
- before/after comparison foundation;
- Hire Expert workflow.

PDF is secondary and must not block MVP.

============================================================
8. REPOSITORY / MODULE STRUCTURE
============================================================

Evolve pragmatically toward:

/
  AGENTS.md
  REQUIREMENTS.md
  ARCHITECTURE.md
  SECURITY.md
  ROADMAP.md
  PLANS.md
  MASTER_EXEC_PLAN.md
  README.md

  docs/
    MASTER_PRODUCT_SPEC.md

  apps/
    audit-service/

  packages/
    contracts/
    scanner/
    discovery/
    metrics/
    rules/
    report-engine/
    shared/

  wordpress/
    gcreation-performance/

  ops/
    dev/

  tests/

  .ops/

Do not reorganize already-working code merely for aesthetics.

============================================================
9. PERSISTENT PROJECT MEMORY
============================================================

Do not rely on this chat as the permanent source of truth.

Persist this product specification into the repository.

Maintain at minimum:

AGENTS.md
REQUIREMENTS.md
ARCHITECTURE.md
SECURITY.md
ROADMAP.md
PLANS.md
MASTER_EXEC_PLAN.md
docs/MASTER_PRODUCT_SPEC.md

Purpose:

AGENTS.md
= durable agent rules.

MASTER_PRODUCT_SPEC.md
= complete durable product/business/technical specification.

MASTER_EXEC_PLAN.md
= changing execution state.

A completely new Codex session must be able to resume this project from repository state alone.

============================================================
10. AGENTS.md RULES
============================================================

AGENTS.md must include durable rules such as:

1. Never fabricate measurements.
2. Never fabricate scan progress.
3. Never invent a plugin/root cause without supporting evidence.
4. Separate measurement from explanation.
5. Deterministic rules must work without paid AI.
6. Public URLs are hostile input.
7. SSRF protection is mandatory.
8. Never commit credentials.
9. Never log authentication secrets.
10. Never touch production from DEV work.
11. Test material features.
12. Prefer simple architecture.
13. Preserve replacement boundaries.
14. Avoid speculative infrastructure.
15. Human approval remains required for risky live-site changes.
16. Do not declare success without observable validation.

Keep temporary milestone state out of AGENTS.md.

============================================================
11. MASTER_EXEC_PLAN.md
============================================================

Maintain:

- project objective;
- current version;
- current milestone;
- completed milestones;
- in-progress work;
- next milestones;
- acceptance criteria;
- test status;
- known bugs;
- blockers;
- discovered constraints;
- architecture decisions;
- deployment state;
- Git state;
- human actions;
- next recommended action.

Update continuously.

============================================================
12. AUTONOMOUS EXECUTION LOOP
============================================================

Operate continuously using:

Inspect
→ Plan
→ Implement
→ Static Check
→ Test
→ Fix
→ Retest
→ Document
→ Commit
→ Push
→ Continue

Do not ask what to do next after every milestone.

For safe reversible technical decisions:

choose the simplest defensible option,
document it,
continue.

Stop only for a genuine human-only blocker.

============================================================
13. HUMAN ACTION PROTOCOL
============================================================

When human action is needed create/update:

.ops/ACTION_REQUIRED.md

Use:

STATUS:
PRIORITY:
BLOCKS:
WHY HUMAN ACTION IS REQUIRED:
FILES TO REVIEW:
EXACT ACTION:
EXACT COMMAND OR UI PATH:
EXPECTED RESULT:
VERIFICATION:
SAFE TO CONTINUE WITHOUT THIS ACTION:

Do not repeatedly request the same action.

Continue every independent task possible.

============================================================
14. FIRST PRIVILEGED DELIVERABLE — SAFE DEV DEPLOYMENT KIT
============================================================

Create:

ops/dev/install-root.sh
ops/dev/deploy-dev.sh
ops/dev/gcreation-perf-dev-deploy.service
ops/dev/gcreation-perf-dev-deploy.path
ops/dev/nginx-dev.conf.example
ops/dev/README.md

Do NOT execute privileged files yourself.

The human owner will review and install them once.

After installation Codex should request DEV deployment through:

.ops/deploy-dev.request

Deployment result/state must be readable through:

.ops/deploy-dev.status

Installed privileged files must become root-owned and non-writable by codexperf.

============================================================
15. PRIVILEGED DEPLOYMENT SECURITY
============================================================

Trusted repository:

/home/codexperf/projects/gcreation-performance

Only allowed WordPress plugin deployment destination:

/var/www/vhosts/gcreation.agency/dev.gcreation.agency/wp-content/plugins/gcreation-performance/

The privileged deployment mechanism must:

- validate fixed paths;
- reject unsafe symlinks/path substitution;
- not execute arbitrary user-supplied root commands;
- never expose Docker socket;
- never give Docker group access;
- never touch production;
- never touch another domain;
- never overwrite complete WordPress;
- preserve actual Plesk ownership/group;
- support rollback;
- use deployment locking;
- write deployment status.

============================================================
16. SERVER RESOURCE CONTRACT
============================================================

Observed host baseline:

24 logical CPUs
approximately 13 GiB RAM
approximately 5.3 GiB MemAvailable at baseline
4 GiB swap
approximately 3 GiB swap already occupied
ample disk available

This is a shared live Plesk server.

Initial audit-runtime ceiling:

approximately 4 CPU total maximum

approximately 1700 MB RAM total maximum

browser scanning concurrency:

1

No uncontrolled Chromium concurrency.

No browser-process leaks.

No unbounded logs or artifacts.

Runtime limits should be externally enforced by trusted deployment/runtime configuration.

============================================================
17. PLAYWRIGHT / BROWSER RUNTIME
============================================================

Use a verified official Playwright runtime.

Pin compatible exact versions of:

- Playwright npm package;
- official Playwright runtime/container.

Do not blindly use latest.

Document the versions.

Runtime must be:

- non-root;
- non-privileged;
- no Docker socket;
- no host-root mount;
- no unrelated Plesk mounts;
- no-new-privileges;
- minimal capabilities;
- PID limited;
- CPU limited;
- RAM limited.

============================================================
18. DEV SERVICE
============================================================

Audit service binds only to:

127.0.0.1:3101

Required:

GET /health

Return HTTP 200 and structured JSON.

Example:

{
  "ok": true,
  "service": "gcreation-performance",
  "environment": "development",
  "version": "..."
}

Do not expose port 3101 publicly.

============================================================
19. DEV PLESK REVERSE PROXY
============================================================

Generate config for:

https://dev.gcreation.agency/perf-engine/

to proxy:

http://127.0.0.1:3101/

Support:

regular APIs
Server-Sent Events

Disable buffering/caching where required for SSE.

Do not change Plesk yourself.

Human owner will apply configuration manually.

============================================================
20. FREE SCAN
============================================================

Initial free scan analyses:

Homepage

plus:

one ecommerce product page where discoverable

otherwise:

one useful internal page.

Use cheap discovery before browser work.

Preferred sequence:

validate URL
→ DNS/IP safety
→ reachability
→ sitemap
→ sitemap indexes
→ URL discovery
→ platform detection
→ classification
→ representative page selection
→ browser scan.

Homepage:

Playwright/network analysis
+
Lighthouse.

Product/important page:

Playwright/network analysis initially.

Do not run Lighthouse unnecessarily on every URL.

============================================================
21. LIVE SCAN EXPERIENCE
============================================================

Use genuine progress.

Prefer SSE.

Possible events:

scan.started
job.queued
site.connected
platform.detected
sitemap.discovered
url_count.completed
homepage.started
resources.discovered
images.analyzed
network.analyzed
server.analyzed
homepage.completed
product.discovered
product.started
product.completed
lighthouse.started
lighthouse.completed
rules.started
rules.completed
report.ready
scan.failed

Never fabricate numbers or progress.

============================================================
22. QUEUE
============================================================

Browser scan concurrency:

1.

If many customers submit scans:

queue them.

Do not spawn uncontrolled Chromium instances.

Support persistent job states such as:

PENDING
RUNNING
COMPLETED
FAILED
WAITING_FOR_RESOURCES
RETRYING where useful.

Track:

priority
attempts
created_at
started_at
finished_at

Bound retries.

No infinite retry loop.

Paid jobs should support higher priority than free jobs.

============================================================
23. SSRF SECURITY — RELEASE BLOCKER
============================================================

Only allow:

HTTP
HTTPS.

Block:

localhost
127.0.0.0/8
::1
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
link-local addresses
private IPv6 equivalents
cloud metadata endpoints
internal hostnames
unsupported schemes.

Resolve hostname before access.

Validate resulting IP.

Revalidate every redirect destination.

Protect reasonably against DNS rebinding.

Public scans must not reach:

localhost services
Plesk internal services
Docker internal services
local database
local Redis
server metadata endpoints
internal audit API.

Use:

request timeout
navigation timeout
overall audit timeout
redirect limit
resource-size controls
bounded retries
browser cleanup
temporary-file cleanup.

============================================================
24. WEBSITE DISCOVERY
============================================================

Use:

sitemap.xml
sitemap indexes
WordPress sitemaps
canonical URLs
internal links
WooCommerce clues.

Classify where possible:

homepage
page
product
product category
blog post
category
cart
checkout
account
search
other.

Store discovered URL count and representative samples.

============================================================
25. FULL WEBSITE AUDIT
============================================================

Full Website Audit does NOT mean Lighthouse every URL.

Use:

all discovered URLs
→ lightweight validation/classification

representative/commercially important pages
→ deep Playwright/network analysis

selected important pages
→ Lighthouse where justified.

Keep compute predictable.

============================================================
26. METRICS
============================================================

Normalize where technically reliable:

HTTP status
redirects
TTFB
page timing
request count
transferred bytes
resource bytes
JS requests/bytes
CSS requests/bytes
image count/bytes
font count/bytes
third-party requests
failed requests
slow requests
cache headers
compression clues
Lighthouse metrics
LCP
CLS
FCP
TBT
Speed Index.

Never infer measurements that were not observed.

============================================================
27. RULE ENGINE V1
============================================================

Implement high-value deterministic rules for:

slow TTFB
poor LCP
high blocking time
excessive requests
large page weight
large JavaScript payload
large CSS payload
oversized images
modern image opportunity
third-party overhead
render-blocking resources
failed resources
redirect chains
cache problems
compression opportunities
font overhead.

Every issue should contain:

rule_id
category
severity
title
affected_url
evidence
measured_values
threshold
impact
recommendation
verification_method.

Thresholds must be centrally defined and testable.

============================================================
28. EVIDENCE POLICY
============================================================

Never state:

"Plugin X caused this"

unless evidence directly supports it.

When evidence is indirect use:

possible contributor
likely contributor
requires deeper WordPress inspection.

Never fabricate root cause.

============================================================
29. BUSINESS CLAIM POLICY
============================================================

Never claim unsupported revenue or conversion losses.

Do not say:

"You are losing 35% of sales."

Do not say:

"Sales will increase by 40%."

unless customer data and a defensible calculation support that exact scenario.

Use:

performance friction
performance opportunity
engagement risk
conversion friction
paid-traffic efficiency may be affected.

Scenario calculations must be clearly labeled as scenarios.

============================================================
30. SQLITE
============================================================

Use SQLite for MVP.

Use migrations from the beginning.

Support entities/tables approximately:

sites
audits
audit_pages
metrics
issues
recommendations
reports
jobs
audit_events
customers
orders
expert_tasks.

Use WAL where appropriate.

Do not introduce PostgreSQL yet.

============================================================
31. WORDPRESS PLUGIN
============================================================

Plugin source:

wordpress/gcreation-performance/

Use WordPress security standards:

capability checks
nonce validation
sanitization
escaping
prepared DB APIs
REST/AJAX permission checks.

Do not expose privileged audit-management endpoints publicly.

Public scan endpoints require anti-abuse controls.

============================================================
32. WORDPRESS ADMIN
============================================================

Keep initial admin simple:

Performance Doctor

Dashboard
Scans
Paid Audits
Expert Orders
Reports
Failed Scans
Settings

Do not build a large ERP.

============================================================
33. FREE REPORT
============================================================

Free report should create real value.

Show approximately:

Performance Health Score

Critical findings
Important findings
Optimization opportunities

Show top meaningful findings.

Indicate additional findings available through deep analysis.

Do not hide evidence required to establish trust.

============================================================
34. WOOCOMMERCE
============================================================

WooCommerce remains commerce source of truth.

Paid scopes:

Major 5 Pages Audit
Full Website Audit

Solution modes:

Self Fix
Hire gCreation Expert.

Store order metadata such as:

Audit ID
Website URL
Analysis Scope
Detected URL Count
Pricing Tier
Solution Mode
Report State.

Payment-completion processing must be idempotent.

Do not require live payment secrets during DEV.

Use test/manual DEV payment flow.

============================================================
35. REPORT ACCESS
============================================================

Avoid building a full customer account system for MVP unless necessary.

Use a secure opaque report token.

Combine with appropriate order/contact/session verification.

Do not expose private customer information in report URLs.

Use strong random tokens.

Rate-limit verification attempts.

Design so OTP can be added later.

============================================================
36. INTERACTIVE FIX CENTER
============================================================

Paid report should show for each issue:

severity
problem
evidence
affected page
measured value
why it matters
recommended action
step-by-step fix
verification method.

Support foundation for:

Mark as Fixed
Test Again
Before / After
Hire Expert.

A checkbox does not constitute technical verification.

Retest is the verification surface where applicable.

============================================================
37. EXPERT WORKFLOW
============================================================

Customer can request:

Hire gCreation Expert.

Reuse existing audit evidence.

Do not restart diagnosis from zero.

ExpertTask states may include:

Pending
In Review
In Progress
Waiting
Completed
Retest Required
Verified.

Risky live website changes require human approval.

============================================================
38. FIRST-100 ANALYTICS
============================================================

Track privacy-conscious events such as:

scan submitted
scan completed
scan failed
WordPress detected
WooCommerce detected
discovered URL count
performance metrics
rules triggered
free report viewed
paid package selected
paid conversion
solution mode
expert request
retest usage.

Do not retain unnecessary sensitive browser artifacts.

============================================================
39. RAW ARTIFACT RETENTION
============================================================

Free scan:

collect
→ normalize
→ persist useful evidence/metrics
→ delete unnecessary raw artifacts.

Paid/debug artifacts may have limited configurable retention.

Avoid unbounded disk usage.

============================================================
40. LOGGING
============================================================

Use structured logs for:

audit lifecycle
job lifecycle
URL security rejection
browser crash
Lighthouse failure
rules
WooCommerce integration
report generation
deployment.

Never log:

passwords
auth cookies
payment secrets
API credentials
private report tokens.

Apply log rotation/size limits.

============================================================
41. RESOURCE GUARDS
============================================================

Before launching heavy browser work:

check whether system pressure is safe.

If resources are unsafe:

do not force Chromium.

Keep job:

WAITING_FOR_RESOURCES

and retry using bounded logic.

Thresholds must be configurable and documented.

============================================================
42. TOOLCHAIN
============================================================

Host currently has a very recent Node runtime.

Do not assume all dependencies support it.

Use reproducible pinned runtime where browser tooling requires it.

Use package-lock.json.

Avoid floating critical dependency versions.

============================================================
43. TESTING
============================================================

Unit tests must include:

URL parsing
scheme validation
private-IP blocking
redirect target validation
pricing tiers
metric normalization
rule thresholds
report authorization helpers.

Integration tests should cover:

SQLite migrations
audit lifecycle
job lifecycle
discovery
API
SSE
WooCommerce integration where practical.

Security tests must cover:

localhost rejection
private network rejection
redirect-to-private rejection
invalid scheme rejection.

E2E target flow:

submit controlled public URL
→ progress
→ free report
→ choose package
→ create DEV/test WooCommerce order
→ paid audit
→ secure report
→ expert request.

Do not use unrelated real customer websites as test targets.

============================================================
44. QUALITY GATES
============================================================

Expose predictable commands where appropriate:

npm ci
npm run format:check
npm run lint
npm run typecheck
npm test
npm run build

Do not silence valid failures.

Do not delete legitimate tests merely to achieve green status.

============================================================
45. GIT
============================================================

Active branch:

develop

Future production:

main.

Do not modify main during MVP development.

Commit meaningful milestones.

Push completed safe work to:

origin/develop.

Never commit secrets.

============================================================
46. NORMAL DEPLOYMENT LOOP AFTER ROOT KIT INSTALL
============================================================

Normal future loop:

Implement
→ Test
→ Commit
→ Push
→ request DEV deployment
→ root-owned deployment watcher runs
→ read deployment status
→ inspect health
→ fix if required
→ redeploy
→ continue.

Codex must never become root.

============================================================
47. EXPECTED ROOT DEPLOY PROCESS
============================================================

The trusted deployment process should approximately:

1. obtain deployment lock;
2. validate trusted paths;
3. reject unsafe symlink/path substitution;
4. create timestamped release;
5. copy trusted source;
6. run deterministic build/tests;
7. reject failed build;
8. start constrained DEV audit runtime;
9. bind only 127.0.0.1:3101;
10. verify /health;
11. PHP-lint WordPress plugin;
12. back up prior plugin version;
13. deploy only gcreation-performance plugin;
14. preserve Plesk owner/group;
15. verify DEV website health;
16. rollback critical failure;
17. retain only a small number of releases;
18. write .ops/deploy-dev.status.

============================================================
48. MILESTONES
============================================================

Proceed approximately:

M0.1
Inspect and reconcile existing repository.

M0.2
Persist master specification.

M0.3
AGENTS + architecture/security docs.

M0.4
MASTER_EXEC_PLAN.

M0.5
Safe DEV deployment kit.

M0.6
Node/TypeScript workspace.

M0.7
Fastify /health.

M0.8
SQLite migrations.

M0.9
Audit/job lifecycle.

M0.10
SSRF validation.

M0.11
Website/sitemap discovery.

M0.12
Page classification.

M0.13
Playwright scanner.

M0.14
Network metric normalization.

M0.15
Lighthouse.

M0.16
Rule Engine V1.

M0.17
SSE progress.

M0.18
Free-report API.

M0.19
WordPress plugin foundation.

M0.20
Live scan UI.

M0.21
Free report UI.

M0.22
Site-size calculation.

M0.23
Trusted pricing/package selection.

M0.24
WooCommerce integration.

M0.25
Paid audit lifecycle.

M0.26
Secure report access.

M0.27
Interactive Fix Center.

M0.28
Retest/before-after foundation.

M0.29
Expert flow.

M0.30
First-100 analytics.

M0.31
Security/E2E/resource validation.

M0.32
DEV release candidate.

============================================================
49. FUTURE — DO NOT BUILD YET
============================================================

Preserve extension points but do not implement unless an MVP blocker genuinely requires them:

PostgreSQL
Redis
BullMQ
R2/S3
paid AI diagnosis APIs
deep WordPress connector
database/PHP profiling
subscriptions
continuous monitoring
white-label agency features
geographic testing
automatic live optimization
mobile applications
public API.

First-100 data decides these priorities.

============================================================
50. DEV DEFINITION OF DONE
============================================================

The DEV MVP is complete only when observable evidence demonstrates:

1. public URL submission works;
2. dangerous/internal URLs are rejected;
3. redirect SSRF protection is tested;
4. jobs persist;
5. concurrency remains 1;
6. genuine progress is visible;
7. website discovery works;
8. sitemap discovery works;
9. homepage browser analysis works;
10. product discovery works where applicable;
11. Lighthouse metrics work;
12. normalized metrics persist;
13. deterministic rules create evidence-backed findings;
14. free report renders;
15. WordPress plugin works on DEV;
16. trusted package/pricing selection works;
17. WooCommerce DEV checkout works;
18. paid audit creation is idempotent;
19. secure paid-report foundation works;
20. Interactive Fix Center works;
21. expert request works;
22. first-100 analytics are recorded;
23. critical automated tests pass;
24. DEV deployment succeeds;
25. internal health succeeds;
26. public /perf-engine/health succeeds after human proxy setup;
27. runtime resource limits are active;
28. browser concurrency remains bounded;
29. production was never touched;
30. develop is committed and pushed;
31. MASTER_EXEC_PLAN accurately reflects final state.

============================================================
51. BLOCKER POLICY
============================================================

Only declare a project blocker when:

- root/Plesk/UI authority is truly required;
- a missing external credential is genuinely required;
- a financial or irreversible business decision is required;
- the security boundary would otherwise need to be violated;
- required infrastructure genuinely does not exist;
- or all safe implementation paths have been exhausted.

When blocked:

document evidence,
create/update ACTION_REQUIRED,
state exactly how to unblock,
continue all independent work.

============================================================
52. IMMEDIATE START PROCEDURE
============================================================

Start now.

First:

1. inspect the current repository and Git history;
2. preserve valid existing work;
3. compare existing work against this specification;
4. persist this specification into docs/MASTER_PRODUCT_SPEC.md;
5. create/update AGENTS.md;
6. create/update REQUIREMENTS.md;
7. create/update ARCHITECTURE.md;
8. create/update SECURITY.md;
9. create/update ROADMAP.md;
10. create/update PLANS.md;
11. create/update MASTER_EXEC_PLAN.md;
12. remove obsolete blocker status if this specification resolves it;
13. build/test the safe DEV deployment kit;
14. create ACTION_REQUIRED only for the genuine root/Plesk actions;
15. continue all non-privileged implementation;
16. run tests;
17. fix failures;
18. commit meaningful milestones;
19. push them to origin/develop;
20. continue autonomously toward the DEV Definition of Done.

Do not merely describe what you intend to do.

Create files.
Write code.
Run tests.
Inspect failures.
Fix failures.
Update project state.
Commit.
Push.
Continue.