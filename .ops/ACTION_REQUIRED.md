STATUS:
P1 HUMAN_CAPABILITY_GATE — CONSTRAINED HUMAN IMAGE-UPGRADE GATE

Independent security review PASS recorded for exact patch1bfe3e0c; approved runtime.Dockerfile three-directory offline chmod implemented. Candidate 0ac34ba50ab3192abfe2ae425c4283879484258e passes exact-archive source regression (59 Python,26 TypeScript,4 gateway;16 commands exit0). New image NOT_BUILT; actual root-owned image/UID10001 positive and root0700 negative acceptance PENDING_HUMAN. P1 IN_PROGRESS / full independent review PENDING; last consumed runtime repair_cycle1, REPAIR_1 failed/consumed1/1, REPAIR_2 deployment0/1, retries0, INITIAL consumed; P2–P7 NOT_STARTED; production/main untouched. Next allowed action: Human review and explicit authorization/execution of the constrained fresh-image upgrade gate ops/dev/REPAIR_2_IMAGE_UPGRADE_GATE.md; no deployment request/image/promotion by Codex.

ACTION FILE:
ops/dev/REPAIR_2_IMAGE_UPGRADE_GATE.md

HUMAN ACTION:
Review and explicitly authorize the proposed fresh-stage image build/isolated acceptance/atomic DATA promotion procedure, then perform only that constrained gate and return its complete sanitized proof. Current security PASS authorizes source/regression only; it does not authorize these privileged actions. The missing root capability and latest human source-only scope require this stop. No automatic installer/image/request action by Codex.

PROHIBITED HERE:
Deployment request, REPAIR_2 attempt, old-image/container in-place chmod, installer/prepare_image/seal rerun, failed evidence cleanup, unrelated trusted/secret/unit/network/WordPress/Plesk/nginx change, P2, production/main.
