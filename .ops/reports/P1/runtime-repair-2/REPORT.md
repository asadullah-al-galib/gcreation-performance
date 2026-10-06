# P1 REPAIR_2 source candidate — pre-image / predeployment handoff

STATE: HUMAN_CAPABILITY_GATE. SOURCE/REGRESSION: PASS. IMAGE/RUNTIME: NOT_RUN / PENDING_HUMAN. Full P1 independent review remains PENDING.

The human independent security disposition PASS accepts proposal3992494 and exact patch SHA2561bfe3e0c08b6d2b456dd494a7240754affcdce56f3e52c1eebd1762089ba41ac. That source/regression authorization has been implemented, with no privileged operation. Approval is not image build/promotion/deployment/runtime acceptance. The reviewed proposal package, previous review artifacts, accepted diagnostics and old oversight events remain unchanged.

## Proven failure and exact correction

Mechanism UID10001_DIRECTORY_TRAVERSAL_FAILURE; defect class image-packaging/permission, classification SECURITY_CRITICAL (SECURITY, RELIABILITY, MVP_RELEASE). In the pinned old image, the correct reviewed gateway file exists root:root0644/matching SHA, but root:root0700 ops, ops/dev, ops/dev/trusted deny UID10001 traversal/read/import. Node returns MODULE_NOT_FOUND; official runtime readiness times out. The final proof is retained in gateway-repair-2-proposal/FINAL_ROOT_CAUSE.json, with the human evidence. No unsupported cause is inferred.

Exactly one implementation line was added in the existing offline RUN before trusted compilation:

```dockerfile
 && chmod 0755 ops ops/dev ops/dev/trusted \
```

No recursive chmod, chown, host-context permission change, snapshot relaxation, gateway byte/path change, dependency/secret/network/SSRF/seccomp/cgroup/resource change. This explicitly reviewed frozen image-packaging correction preserves the V4 enforcement model. SECURITY_BOUNDARY_VERIFICATION.json hashes45 unchanged/control input files relative to accepted134ddfbe, with only runtime.Dockerfile different.

## Exact candidate identities

- Candidate commit: `0ac34ba50ab3192abfe2ae425c4283879484258e`.
- Parent: `3992494df7776be6114fd89a170112071eb25402` (preserves all prior committed develop work).
- Candidate changed files: `ops/dev/runtime.Dockerfile`, `tests/test_gateway_image_permissions.py`, `tests/gateway-image-permissions-probe.mjs`.
- Dockerfile before SHA256: `b57d39dc4bb75e625c308841a3e71be23718f4e1dde1aab25b9d6b974939dc07`.
- Dockerfile after SHA256: `21ee8641969bc2eb92a91d1dcde28ed90e6420433bb022f1a25d1237c7eec152`.
- Gateway unchanged SHA256: `d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c`.
- Archive DATA path: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-0ac34ba50ab3192abfe2ae425c4283879484258e.tar.gz`.
- Archive SHA256: `958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced`.
- Source manifest SHA256: `bfd511f25b48b5a335badc0547b846eda2189e19dce9039b2e56a6e744120ae7`.
- Expected canonical snapshot digest: `44b5b3b45036ce787f2b9c4ecb20ae21c37db323904b6f18c7c341b976d528ae`.
- Exactly182 regular archive members /181 committed blobs;335338 compressed bytes. Two independent exports byte-identical; every member equals committed Git bytes, marker exact, no cache/links/special entries. No mutable workspace-byte artifact.
- Manifest uses sorted string paths; canonical digest uses sorted Python Path order with path/NUL/raw content SHA. SOURCE_MANIFEST.sha256 includes the generated candidate marker.
- New immutable image status: **NOT_BUILT; ID null**. Old immutable image retained: `sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24`.

SOURCE_DIFF.patch is the exact three-file candidate diff. Governance, acceptance, report, checkpoint and proposed human gate are committed in the later handoff transaction; they are not new application source or the candidate archive. Historical state text within the candidate archive describes the prior checkpoint and does not override the current gate.

## Source checks and necessary image checks

Targeted fixture6/6 PASS first. Existing Python53/53 PASS (deployment12,V3 security21,V4 security13,bytecode4,source-permissions3). TypeScript26/26 PASS; gateway4/4 PASS. Unique automated tests89, no failures/skips. All16 exact extracted-candidate commands exit0, including formatting, full lint, typecheck, tests, application build, trusted TypeScript compile, PHP syntax/integration and shell syntax. CANDIDATE_TEST_RESULTS.json records exact commands/environment/log paths/log hashes. Lint repeats46 already-counted Python tests; they are not double-counted.

The focused test recreates umask0077 reviewed image inputs, rejects the three0700 ancestors, runs the exact Dockerfile chmod command and proves only those three modes change, no other owner/mode/hash/path changes, gateway0644/SHA exact, host context remains private/unchanged, agent-UID dynamic import succeeds. It also proves an inaccessible ancestor yields ERR_MODULE_NOT_FOUND, rejects altered/missing/writable gateway inputs and refuses image CLI identity/permission overrides. Existing verifier/archive/dependency/bytecode/security modules remain byte-identical and their fail-closed regressions PASS.

**These are ordinary-user source/packaging fixtures, not root:root image proof.** The local0700 test detects the contract violation and models different-UID denial; mode000 supplies an actual nonprivileged access/import failure. Actual root0700/UID10001 reproduction and corrected-image root:root0755/0644/UID10001 read/import are NOT_RUN. The read-only probe's fixed CLI requires actual10001:10001, all seven root-owned rows, no group/other write, matching gateway hash and successful dynamic import. The human gate MUST execute it in the fresh image, plus the actual root0700 negative, and compare old/new trusted-tree metadata/content. Those pending checks cannot be claimed using source fixtures.

## Human image-upgrade gate and preservation

Canonical gate: `ops/dev/REPAIR_2_IMAGE_UPGRADE_GATE.md`. Proposed procedure, pending human review/authorization; no privileged executor/bridge was added. It uses a fresh protected candidate archive/map/snapshot with exact preflight/no-bytecode, a fresh root-private fixed-input context, bounded reviewed fresh-image build, isolated UID10001 checks and old/new tree comparison. Only after explicit scoped authorization and all checks PASS does its proposed human-only promotion replace runtime-image-id and matching installed Dockerfile DATA with backups and explicit failure rollback. Old context/image/tags/stages/controller/units/dependencies/secrets/networks/data/releases/status remain preserved. No installer/prepare_image/seal rerun, existing image/container chmod or deployment request.

No build-capability shortcut: if the operator cannot enforce reviewed bounded build resources/logs, stop before building for a separate scoped capability decision. Agent privilege is forbidden. Source PASS does not authorize an unreviewed root path. Snapshot stays immutable; the only image chmod is in the reviewed offline Dockerfile layer.

Counters remain INITIAL consumed; REPAIR_1 failed/consumed1/1; repair_cycle1 (last consumed runtime cycle); REPAIR_2 deployment0/1; retries0. Candidate preparation has not consumed a runtime attempt or reset any budget. P1 runtime acceptance remains FAIL from the previous attempt, independent review PENDING; P2 NOT_STARTED. No internal/public health, sandbox/cgroup, container/network, release/request-consumption or rollback/retention P1 completion is granted by these source checks. Production/main untouched.

STOP at HUMAN_CAPABILITY_GATE. No new-image build/promotion/request occurs in this transaction. External oversight PENDING/non-blocking; the checkpoint is persisted to latest JSON/MD and event0008 before any future image/deployment action.
