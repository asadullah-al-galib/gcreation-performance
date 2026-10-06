# P1 REPAIR_1 — source traversal under private service UMask

REPAIR STATE: REVIEW_READY. P1 BLOCKED / REPAIR_1 REVIEW; orchestrator SECURITY_REVIEW_REQUIRED. Independent repair/full-Part reviews PENDING. Deployment authorization NO. P2–P7 NOT_STARTED; production/main untouched.

## Failing requirement and evidence

P1-BUILD-01 / D24–D27: reviewed source must be readable by the constrained offline UID/GID10001 builder without relaxing V4 controls. The single separately approved deployment of source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b / archive80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929 FAILED at non-root-build: controller build_command exit1, RuntimeError, rollback=false. Request1/1 consumed; retries0. [HOST_FAILURE.json](HOST_FAILURE.json) records HUMAN_ATTESTED / REAL_DEV_VERIFIED failure/inspection only. No raw subprocess error or deployed snapshot digest was supplied. Installation PASS and prior -I -B review/host validation remain valid historical installation evidence; neither grants this candidate PASS.

The operator observed root-owned release/source0700 and UID10001 output0700. Request/claim/active release/runtime containers are absent; failed release and DEV networks retained. No previous successful runtime existed, so rollback=false does not establish a rollback bug. Old/fresh root review stages, installed components, source artifact and status remain untouched by this preparation.

## Confirmed root cause

The unchanged deploy.service has UMask=0077. Its mkdir(mode=0755) calls for release/source and artifact parent directories are filtered to0700. artifact_snapshot explicitly normalizes source files0644 but originally did not normalize directories. The unchanged non-root/network=none/read-only builder begins cp -R /source/. /app/; UID10001 cannot list/traverse root-owned0700 source directories. [ROOT_CAUSE_REPRODUCTION.txt](ROOT_CAUSE_REPRODUCTION.txt) shows release, source and nested apps/packages/ops/tests directories0700 under ordinary-user UMask0077; [BASELINE_REGRESSION.txt](BASELINE_REGRESSION.txt) records the expected regression failure before repair. This confirms the permission defect and matches the human observation; it does not invent an unobserved cp error string. Fixture ownership is ordinary UID, with other-user r/x modeled; no actual root/UID change, Docker or controller entrypoint was used.

## Minimal repair and exact source diff

Candidate 134ddfbe393168ce7cef99c44817329c84a8d6eb; exactly one parent 08b395cf08523dbc5ab27f744d174b8a19bb2b4b. [SOURCE_DIFF.patch](SOURCE_DIFF.patch) is the zero-context exact Git diff. Changed candidate source files:

- ops/dev/deploy_controller.py: seven added lines; explicit release/source chmod0755 and traversal of newly extracted parent directories up to (excluding) the already-normalized source root. Source files retain0644. No source chown, process UMask change, chmod0777, write access for group/other, privileged execution or unrelated diagnostic change.
- tests/test_source_permissions.py: three deterministic tests for actual root-creation AST plus actual archive extraction under0077, all nested directory/file modes and unchanged ordinary fixture ownership, other-UID permissions, private state0700/global UMask, fail-closed hash/dependencies and exact non-root/offline/read-only/security/resource builder command.
- MASTER_EXEC_PLAN.md and ROADMAP.md: format-only Markdown table spacing/divider width normalization relative to the accepted source. No words/status/criteria changed in these source-candidate documents. Initial exact-source format:check failed on these inherited tables; the unchanged builder runs that gate, so formatting was necessary to prevent a known subsequent build failure. Initial candidate fb4cba7a8327b0117fffcb27613c4945526597c7 and failed validation are retained as preparation evidence, not another deployment/repair cycle.

The only changed privileged/security implementation is ops/dev/deploy_controller.py. Its [PRIVILEGED_DIFF.patch](PRIVILEGED_DIFF.patch) contains only directory normalization. Existing develop governance commits are retained; source is integrated through merge ancestry, with current state in a later handoff commit. Archive governance text is historical baseline metadata, never deployment/review authority. Use the exact candidate archive, not the latest handoff tree as installation source.

## Candidate DATA identity

Archive: /home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-134ddfbe393168ce7cef99c44817329c84a8d6eb.tar.gz

SHA256: d2c69e1a49342ae09867bd206e39e89d969c8d0e39eb3c6e9b1eaaf93c1e68b0

Source manifest: SOURCE_MANIFEST.sha256; SHA256 b8900ea6c39fa2baf3b3481263e6ef778e3f5eb54fcb019ffb600ca6014d5a95

Expected canonical snapshot digest: 8425d68350e9c9d93f941f62591142cd21a68835b35df188ee63cc415b3054b5

Regular members: 106; committed blobs verified: 105; deterministic re-export: IDENTICAL_BYTES. [ARCHIVE_VERIFICATION.json](ARCHIVE_VERIFICATION.json) verifies every archived blob against the commit and marker. The digest is computed from sorted relative paths, NUL and raw content SHA256 exactly as the unchanged controller snapshot_digest; it is not an observed deployed/root snapshot. New archive/image installation/deployment has no human approval.

## Tests and preserved boundary audit

Final exact candidate tests/results: CANDIDATE_TEST_RESULTS.json and CANDIDATE_REGRESSIONS.txt. Run each Python suite in an isolated ordinary-user process, plus unchanged Node/PHP/shell gates on an extracted source fixture with local frozen dependencies; no Docker/install/request/networked customer work. Final results:53/53 Python tests (new permissions3, deployment12, V3 review21, V4 review13, installer bytecode4),26/26 TypeScript tests and4/4 gateway socket tests PASS; format:check, lint:ts, typecheck, build, trusted TypeScript compilation, PHP syntax/integration, bash/sh syntax all exit0. All15 final isolated commands passed. PYTHON_REGRESSIONS.txt and OTHER_REGRESSIONS.txt retain initial develop validation, including the inherited formatting failure. INITIAL_CANDIDATE_REGRESSIONS.txt retains first-source validation before formatting correction; no test was weakened.

V4_BOUNDARIES.json:50 previously tracked security-influencing files checked against 08b395cf08523dbc5ab27f744d174b8a19bb2b4b;49 byte-identical and only controller normalization changed. All other committed source differences are the regression and the two formatting-only tables. Builder flags/limits, all runtime start/network/membership/image/secret/self-host/health/retention/rollback functions, archive validation/anchoring/hash/marker/dependency checks, installed entry guard, systemd UMask0077/slice, seccomp, Dockerfile/base pins, gateway/proxy/SSRF, human-only PHP/health-only nginx and accepted -I -B installer remain unchanged. Local/static audit PASS does not grant independent review or deployed acceptance. Root ownership follows unchanged root creation; the repair adds no source ownership mutation. /var/lib private parent stays0700; source bind mount stays readonly; only existing nonsecret reviewed source gains its intended read/traversal modes. No security boundary change is required.

## Review and operator stop

This is first bounded runtime repair REPAIR_1 (repair_cycle1), not a failed repair cycle; no new deployment submitted. Review HUMAN_REVIEW_GATE.md and the exact four source files/diff/archive/manifest/expected digest/test/boundary/failure evidence. Independent review and a separate explicit human decision are required before any installed-controller refresh or deployment. Source tests passing do not restore the consumed1/1 authorization.

Do not install/redeploy/clean anything now. The installed controller still belongs to accepted source08b395c and has the observed defect; it must not be bypassed or edited by Codex. If accepted, a later human-approved recovery must stage the new exact archive into a new root-only reviewed snapshot with unchanged archive verification/preflight, preserve both existing root review stages/failed release/status/networks/source artifact and review required root-owned trusted-controller changes. No direct repository module as root, automatic installer rerun, root snapshot reuse/cleanup or Docker/systemd/Plesk/nginx/WordPress mutation is authorized by this report. Existing immutable image identity is historical; no new image identity is assumed. Any update/install/network/release cleanup and next single deployment need their own explicit operator gate. Runtime health/containment/rollback/retention and D24–D27 remain PENDING. STOP.
