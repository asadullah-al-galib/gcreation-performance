FINAL GATEWAY ROOT CAUSE REPORT

EXACT FAILURE MECHANISM:
UID10001_DIRECTORY_TRAVERSAL_FAILURE.

EVIDENCE:
Handoff SHA256 dca7dfa7aa8dfd4f46a248691f2ef311463651583f805b794d2f4d9bf54d7f8c verified exactly. In pinned image f2bb2401..., gateway.mjs exists/root:root0644 and SHA256 d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c equals accepted134ddfbe source. Official installed controller029c5d57... launches exactly node /opt/gcreation-trusted/ops/dev/trusted/gateway.mjs. Root image metadata and UID10001 effective access/import are human-attested isolated read-only diagnostics, reconciled independently with committed hashes and prior evidence.

| Image path | UID:GID | Mode | UID10001 traversal/read result |
| --- | --- | --- | --- |
| / | 0:0 | 0755 | traversal PASS |
| /opt | 0:0 | 0755 | traversal PASS |
| /opt/gcreation-trusted | 0:0 | 0755 | traversal PASS |
| /opt/gcreation-trusted/ops | 0:0 | 0700 | traversal FAIL |
| /opt/gcreation-trusted/ops/dev | 0:0 | 0700 | traversal FAIL |
| /opt/gcreation-trusted/ops/dev/trusted | 0:0 | 0700 | traversal FAIL |
| /opt/gcreation-trusted/ops/dev/trusted/gateway.mjs | 0:0 | 0644 | file read blocked by ancestors |

WHY NODE RETURNED MODULE_NOT_FOUND:
The exact reviewed file exists and is ordinarily world-readable, but UID10001 cannot traverse the root-owned0700 ancestor chain. The path therefore cannot be resolved by the non-root loader. UID10001 existence check reports NO/read FAIL; dynamic import returns ERR_MODULE_NOT_FOUND/exit7. The earlier startup probe reported MODULE_NOT_FOUND/exit1. Missing file, wrong path and content mismatch are excluded. The failure is not an independent0644 file-mode read denial.

WHY REPAIR_1 RUNTIME HEALTH FAILED:
REPAIR_1 restored traversal for mutable build-source directories, allowing the constrained build to finish. It preserved the old immutable image. That image's gateway cannot load under the official10001:10001 user, cannot serve health, and the installed start_runtime readiness loop expires. Earlier fresh/cloned-data app startup and direct health200 exclude an app/persisted-data explanation for this reproduced gateway failure. Gateway→app networking was not reached; no network defect is claimed.

DEFECT CLASS:
image-packaging / permission. Accepted prepare_image directory creation is umask-sensitive; a non-privileged0077 fixture leaves trusted source ancestors0700, matching the observed image directory modes. The Dockerfile copies that tree without normalizing these gateway ancestors.

SMALLEST CORRECTION:
An UNAPPLIED one-line proposal adds `&& chmod 0755 ops ops/dev ops/dev/trusted` inside the existing offline image-build RUN step, after the dependency symlink and before trusted compilation. It changes only those three image directory modes. Root ownership, gateway0644/hash/code/launch path, private host context/snapshot, final non-root user, separate secrets, readonly runtime, dependency/base-image freeze, networks/SSRF/sandbox/resource controls stay unchanged. No recursive chmod/chown, live chmod, writable gateway or release-source gateway mount.

EXACT FILES THAT WOULD NEED CHANGE:
Implementation: ops/dev/runtime.Dockerfile only, one added line. A targeted regression must be added after approval to validate this exact image path/UID10001 import; see TARGETED_REGRESSION_PLAN.md. No repair has been applied to implementation or test sources.

V4 SECURITY BOUNDARY IMPACT:
YES: correcting the reviewed immutable runtime image/trusted gateway packaging changes a frozen image input and requires a new reviewed image identity. SECURITY_REVIEW_REQUIRED. Current boundary and installed code/image remain unchanged; the proposal preserves the enforcement model. Independent review is required before implementation, and a separate constrained human image-upgrade gate will be necessary before runtime deployment.

TARGETED REGRESSION TEST:
Build the reviewed corrected image in the authorized human/constrained environment; inspect exact fixed file/ancestor metadata and hash; run network-none/readonly/cap-dropALL/no-new-privileges/bounded Node dynamic import as10001:10001. Require traversal of every ancestor, file readability and import success; baseline0700 must fail. Keep a restrictive-umask preparation fixture, assert host context privacy and source ownership/hash unchanged, and retain existing gateway/security regressions. Local mode-only proposal fixture PASS is not actual candidate-image acceptance.

REPAIR_2 PLAN:
1. Independent review of this package and exact unapplied patch; no source/image/runtime action before disposition.
2. After approval, apply only the approved line and focused regression; advance the implementation-cycle ledger without resetting consumed attempts. Run targeted and relevant V4/archive/image/gateway/application quality checks. Produce a deterministic source commit/archive/manifest/snapshot and push a predeployment oversight checkpoint.
3. Prepare a separately reviewed human-only fresh image-upgrade gate using immutable root-reviewed inputs; preserve old image/context/stages and installed credentials/baseline/units. No install-root.sh rerun or in-place repair of the old image. Record exact new immutable image ID and verify actual UID10001 import/health before enabling its one request.
4. Only once all source/security/operator gates and tests PASS, submit at most one exact committed-artifact REPAIR_2 watcher request, retries0, then all P1 effective runtime/health/security/resource/identity/retention criteria. No diagnostic deployment; P2 waits for full P1 exit.

COUNTERS / STATE:
INITIAL consumed; REPAIR_1 FAILED/consumed1/1; retries0; REPAIR_2 attempts0; current repair_cycle1 preserved while preparing the review proposal. Source candidate/new archive/new image not yet created. P1 IN_PROGRESS/full independent review PENDING; P2–P7 NOT_STARTED; production/main untouched. STOP: SECURITY_REVIEW_REQUIRED.
