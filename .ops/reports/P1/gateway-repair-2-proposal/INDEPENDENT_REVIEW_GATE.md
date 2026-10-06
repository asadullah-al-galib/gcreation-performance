# Independent security review — unapplied REPAIR_2 proposal

STATE: SECURITY_REVIEW_REQUIRED. This is the explicit user security-rule stop for a frozen immutable-image packaging correction. Review the final cause, pinned-image/UID evidence, exact patch and identities, local fixture limitation, regression plan and controlled recovery constraints. No implementation, source candidate, new archive/image, installation or request is authorized by preparing this package.

Review scope: one added fixed-directory chmod0755 in ops/dev/runtime.Dockerfile's existing offline RUN. The three directories contain reviewed non-secret trusted source and remain root-owned/non-writable by the runtime UID. All input bytes/file0644/source trust/private host paths stay unchanged. Reject any recursive chmod/chown, writable source, launcher change, live image/container edit, secret/network/cgroup/SSRF relaxation or image promotion without its own reviewed operator gate.

Human/independent reviewer returns PASS or HOLD for this exact patch SHA in PROPOSAL_IDENTITIES.json and package CHECKSUMS.sha256, with any concrete findings. A source-proposal PASS permits only the specified source/regression work under the recorded scope; it does not itself grant runtime acceptance or agent privilege. Root/image upgrade remains an operator/constrained-capability action after an exact implemented artifact is available.

INITIAL and REPAIR_1 consumed; REPAIR_1 attempts1/1, retries0; REPAIR_2 attempts0. Do not retry for diagnosis or spend repair2 on this review. P2 not started; production/main untouched. STOP.
