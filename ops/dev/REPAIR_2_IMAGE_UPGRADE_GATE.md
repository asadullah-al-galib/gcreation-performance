# P1 REPAIR_2 — constrained HUMAN IMAGE-UPGRADE GATE

STATUS: PROPOSED / NOT EXECUTED / HUMAN OPERATOR REVIEW AND AUTHORIZATION REQUIRED.

The independent PASS for proposal3992494 and patch1bfe3e0c approves source and regression implementation only. It does **not** authorize this root procedure, an image build/promotion, an installer rerun or a deployment request. The operator must review and explicitly authorize this exact bounded procedure before performing it. Codex stops at HUMAN_CAPABILITY_GATE and executes no privileged component. Classification SECURITY_CRITICAL; mapping SECURITY, RELIABILITY, MVP_RELEASE.

## Pinned DATA and preservation baseline

- Source candidate: `0ac34ba50ab3192abfe2ae425c4283879484258e`; parent `3992494df7776be6114fd89a170112071eb25402`.
- Source archive DATA: `/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-0ac34ba50ab3192abfe2ae425c4283879484258e.tar.gz`.
- Archive SHA256: `958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced`; exactly182 unique regular members.
- Source manifest SHA256: `bfd511f25b48b5a335badc0547b846eda2189e19dce9039b2e56a6e744120ae7`.
- Expected canonical snapshot digest: `44b5b3b45036ce787f2b9c4ecb20ae21c37db323904b6f18c7c341b976d528ae`.
- NEW stage only: `/var/lib/gcreation-perf-review/0ac34ba50ab3192abfe2ae425c4283879484258e`. Abort if already present; do not reuse or delete.
- Old image: `sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24`; retain both its ID and all existing tags/layers. New image ID is NOT_BUILT/PENDING, never inferred from the source hash.
- Installed controller must remain root:root0644/single-link with SHA256 `029c5d5714a13fbdd3565901bdc08341e36319c1ab90cf30ea6d4ab7e58c4039`.
- Old Dockerfile SHA256 `b57d39dc4bb75e625c308841a3e71be23718f4e1dde1aab25b9d6b974939dc07`; candidate SHA256 `21ee8641969bc2eb92a91d1dcde28ed90e6420433bb022f1a25d1237c7eec152`.
- Gateway SHA256 `d9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c` remains exact reviewed bytes/root:root0644.
- Package: `.ops/reports/P1/runtime-repair-2/`; acceptance: `.ops/reports/P1/REPAIR_2_SECURITY_ACCEPTANCE.json`. Independently verify its checksum files and the published checkpoint before root work. The archive includes the candidate's historical governance ledger; this newer gate/checkpoint records the current authorization limits.

Preserve stages8217aa4,08b395c,134ddfbe and controller rollback backup, the installed old build-context, old image/runtime-image-id, dependency-baseline.json, controller, seccomp, units, environment/receiver secrets, failed releases/data/networks, old request/status evidence, WordPress/Plesk/nginx and production/main. No cleanup, status reset, service restart, installer/prepare_image.py/seal rerun, secret regeneration or runtime deployment is included.

## A — verify fresh immutable inputs, without installed changes

1. Require explicit authorization for this gate, an exclusive nonblocking hold of the **existing** protected `/var/lib/gcreation-perf-dev/deploy.lock`, no concurrent operator/deploy service activity, no request or claimed request (lstat/no-follow, including dangling links), watcher active/enabled, and no active official runtime. If any precondition differs, STOP with the exact criterion; do not repair it here.
2. Privately inventory every installed trusted entry, units, image/reference, private environment files, baseline, old context/stages, runtime data, releases/networks and old deployment evidence. Record hash/type/owner/group/mode/link comparisons; never return secrets, private configuration hashes, full inspect, Config.Env or sensitive argv. Verify the existing installed files against the accepted134ddfbe snapshot and pinned identities above. Retain a before inventory for exact after comparison.
3. Use only the reviewed **DATA staging** bootstrap in ROOT_TRUST_TRANSITION.md, adapted to the pinned candidate/hash. The human types/reviews system-standard-library stdin with clean `env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I -B`; never run a workspace module as root and never execute the install block. Stage root:root0700; protected archive and approved.json root:root0600, single-link regular files; all ancestors root-owned/non-symlink/non-writable by group/other. Reject an existing stage, path/link/type/mode mismatch or changed archive.
4. Validate the protected archive **before extraction**: exact SHA/count/marker, unique canonical safe relative regular entries only, no links/special/traversal/credential/bytecode/cache entries; compressed64MiB, expanded96MiB, each file8MiB, total payload64MiB bounds. Require `REVIEW_SOURCE_COMMIT` exactly candidate plus newline. Require the pinned manifest hash (sorted string filenames, `sha256 + two spaces + name + newline`) and canonical digest (sorted Python Path order, UTF-8 relative filename, NUL, raw32-byte content SHA256). The old bootstrap must be augmented with these checks, never weakened; do not use extractall or accept expected hashes from mutable workspace metadata.
5. Extract fresh root-owned0644 snapshot DATA and the exact182-entry approved.json map. Rewalk with lstat, require root-owned protected ancestors/single-link regular files, no extra/missing/cache entries, every byte hash/map/manifest/digest exact. Snapshot remains immutable; no chmod/chown of its trusted paths is the image fix. Only now may the verified snapshot's existing reviewed preflight execute:

   ```sh
   /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I -B \
     /var/lib/gcreation-perf-review/0ac34ba50ab3192abfe2ae425c4283879484258e/snapshot/ops/dev/install_preflight.py \
     /var/lib/gcreation-perf-review/0ac34ba50ab3192abfe2ae425c4283879484258e/snapshot \
     958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced \
     0ac34ba50ab3192abfe2ae425c4283879484258e
   ```

   Capture exact command, time and exit0 privately; reverify snapshot/map/digest and no bytecode after. No verifier bypass, deletion workaround, snapshot reuse or installer run.

## B — fresh image only, followed by isolated acceptance

1. In the NEW protected stage, create a fresh `image-context` root:root0700 with system DATA-copy operations only. Copy the verified candidate Dockerfile as `image-context/runtime.Dockerfile`, and candidate package.json/package-lock.json into the context root. Copy **exactly these nine** verified inputs under `image-context/trusted-source/`:

   ```text
   package.json
   package-lock.json
   tsconfig.json
   ops/dev/trusted/tsconfig.json
   ops/dev/trusted/gateway.mjs
   packages/scanner/src/proxy.ts
   packages/scanner/src/proxy-main.ts
   packages/shared/src/security.ts
   packages/shared/src/auth.ts
   ```

   Explicit root:root0644/single-link files, root:root0700 context/intermediate directories, umask0077. Match every content hash to the verified snapshot/approved map; reject extras/links. Confirm package/lock hashes equal the **unchanged installed** dependency baseline. Do not execute prepare_image.py with a changed DEST or bypass its root guard. Leave the installed old context and baseline untouched.

2. Independently inspect the exact Dockerfile: only the reviewed non-recursive three-directory chmod changes; base image digests/Node/dependency baseline/user/offline trusted compiler unchanged. Build only through the operator-reviewed existing BuildKit path, from this root-only context, with a new unique tag `gcreation-perf-dev-runtime:repair2-0ac34ba50ab3192abfe2ae425c4283879484258e`, never the old tag. No lifecycle/test/release/workspace code may execute as root; the only source compilation is the already reviewed trusted offline compiler step. Network access is limited to the existing reviewed pinned-base/package download steps; trusted compilation remains `RUN --network=none`, npm ci remains ignore-scripts/frozen lock. No extra Dockerfile/chmod/chown/repository inputs.
3. Before any build, require the human's bounded build mechanism/resource budget and log limits to be recorded: one build, no automatic retries, maximum900s, bounded private logs (5MiB, stop on overflow), existing DEV CPU/memory/PID containment. If the installed mechanism cannot enforce these bounds, STOP for a separately reviewed build-capability decision; do not introduce a transient service, daemon reconfiguration or root bridge here. Record exact approved build command, flags, times and exit; this source PASS does not itself approve an unreviewed root build path.
4. Resolve the new image's immutable content ID with whitelisted inspect fields only; record image ID and the verified source/context identities. No old-image overwrite/tag/removal, runtime-image-id replacement or official runtime action yet.
5. Copy candidate `tests/gateway-image-permissions-probe.mjs` as DATA to `STAGE/image-probe.mjs` root:root0644/single-link and hash-compare it. Execute only this read-only module **inside the new image as UID:GID10001:10001**, never as host/root code. One isolated observer, network=none, read-only rootfs, cap-dropALL, no-new-privileges, unchanged verified seccomp, PID64/CPU1/memory256MiB/memory-swap256MiB, existing slice, init, local5MiB/two-file logs and30s deadline. No env-file, credentials, official release/data/network mounts or published ports; only the verified probe DATA bind-mounted read-only at `/image-probe.mjs`. Use immutable new ID, fixed `/usr/local/bin/node /image-probe.mjs`, no CLI overrides. Keep sanitized output/exit and whitelisted isolation identity. It must prove all seven rows, root:root0755 ancestors/no group-other write, root:root0644 gateway/matching SHA, actual UID10001 traversal/read/import PASS. Dynamic import does not run the gateway listener.
6. Mandatory exact-defect negative: create a separate root-private **diagnostic DATA fixture** under the new stage, with ops/dev/trusted root:root0700 and reviewed gateway root:root0644/matching SHA. For one otherwise identically constrained UID10001 observer only, bind that fixture read-only over `/opt/gcreation-trusted/ops`; import the exact fixed file URL with system Node. Require nonzero exit plus ERR_MODULE_NOT_FOUND, while the file demonstrably exists/hash matches and the ancestor is root0700. This is an isolated negative-test mount only; never modify the image, an official container or the runtime launch policy. No deployment attempt is spent. Retain the diagnostic fixture/proof; remove no old evidence.
7. Under the same restrictions, human-only read-only system-Node metadata observers may run as container UID0 to inventory the **old and new** `/opt/gcreation-trusted` trees without importing source, following symlinks, printing environment or accessing official runtime data. Compare content hashes, uid/gid/type/mode/link targets and names (ignore timestamps/inodes); exactly the three approved directories may differ0700→0755. Gateway0644/SHA and every unrelated trusted source/compiled file remain exact. Check unchanged Node/base pins/dependency manifests/baseline and non-root default image user. Any unexpected content or permission difference is HOLD; never fix it live. These observer containers are not application/runtime acceptance.

## C — proposed atomic promotion, only after separate gate authorization and B PASS

This is a proposed **human-only** promotion of the proven image reference and matching Dockerfile DATA, not automatic permission. No deployment request follows this gate. Keep the existing lock throughout checks/promotion/rollback; recheck request/claim absence and no official runtime/service activity before changing any installed pointer.

1. Preserve protected root:root0600/single-link backups of installed `runtime-image-id` and `runtime.Dockerfile` in the NEW stage. Prove old image text/ID and Dockerfile bytes/hash match the baseline; never overwrite existing backup paths. Preserve old image/tag/context and record new provenance privately outside the snapshot.
2. Prepare fresh absent same-directory root-owned0644/single-link temporary DATA files under `/usr/local/lib/gcreation-perf-dev`: candidate Dockerfile exact SHA/bytes and new proven `sha256:<64hex>` image ID plus newline. Check all ancestors/types/modes, same-filesystem rename, no secret content, and exact equality to verified inputs. Rename Dockerfile, then runtime-image-id atomically per file with system utilities only; the pointer switch is last. There is no cross-file atomic transaction: a failure after either rename **must take the explicit rollback branch** before releasing the lock. No installed source/controller execution, tag replacement or service restart/reload.
3. Require installed pointer root:root0644/single-link equals actual new immutable image ID; installed Dockerfile root:root0644/single-link equals the verified candidate. Reverify image/source/snapshot/no-bytecode evidence. Compare the preservation inventory: only these two installed DATA files and the explicitly authorized new stage/context/probe/image/diagnostic resources may differ. All other enforcement/secret/unit/context/runtime/network/WordPress/production state remains unchanged. Watcher still active/enabled, request/claim absent, no new official deployment, attempts0/1, retries0.
4. If any postcheck fails, preserve evidence and while holding the lock validate the two backups/hash/owner/mode/link counts, create new absent same-directory rollback temps root:root0644, restore BOTH original DATA files by verified same-filesystem renames, verify old image pointer/recipe and every preservation criterion, then STOP. Never delete a failed new image/stage or auto-retry the build/promotion. If restoration cannot be verified, stop for a human decision; do not claim success.

## Exact sanitized proof to return

Operator identity/explicit bounded gate authorization, UTC observation times, exact scoped commands and exits; fresh protected archive SHA/count/marker/manifest/map/digest/preflight/no-bytecode; lock/preconditions; old/private backup paths and non-secret hashes/modes/link counts; exact context input/dependency hashes; approved bounded build command/resource/log evidence and exit; NEW immutable image ID; actual UID10001 positive probe output and isolation flags; root0700 negative fixture metadata/hash/import error/exit; old-v-new trusted tree comparison with exactly three mode differences; promotion/rollback result (or NOT_PERFORMED); installed pointer/Dockerfile identities; all other state preserved, watcher/request/claim status, zero official deployments/retries, production/main untouched. No secrets/full inspect/private-config hashes.

Partial proof remains HOLD/PENDING, never P1 PASS. Runtime health/public routes/container/network/resource/rollback-retention acceptance are still required after a separately allowed single candidate-pinned REPAIR_2 watcher deployment. Counters remain INITIAL consumed, REPAIR_1 failed/consumed1/1, repair_cycle1 as last consumed runtime cycle, REPAIR_2 deployment0/1, automatic retries0. P2 NOT_STARTED. Codex must verify complete returned proof and authorization before any later request; this gate itself creates none.
