STATUS:
P1 HUMAN_CAPABILITY_GATE

Exactly one accepted candidate-pinned REPAIR_1 watcher request consumed; terminal FAILED at runtime-health/RuntimeError/rollback=false. Constrained build return0 inferred from reviewed stage progression. Root cause unknown; current read-only runtime diagnostics require an unavailable approved capability. Controller refresh remains PASS. P1 execution IN_PROGRESS / full independent review PENDING; repair_cycle1; REPAIR_1 attempts1/1, automatic retries0; prior INITIAL consumed; P2–P7 NOT_STARTED; production/main untouched. Next allowed step: Obtain bounded sanitized read-only diagnostics; establish exact failed operation/cause before any relevant REPAIR_2 change. No new request or P2. Evidence: .ops/reports/P1/REPAIR_1_DEPLOYMENT_ATTEMPT.json.

HUMAN ACTION:
Designated operator returns one sanitized read-only service traceback/fixed DEV container/image diagnostic bundle under .ops/reports/P1/REPAIR_1_RUNTIME_DIAGNOSTICS_GATE.md; no rerun, retry, restart, cleanup or configuration change.

No root/escalation/Docker socket/group/Plesk-admin or production/main access. Do not rerun refresh/installer/image build, retry consumed request or start P2 before required P1 exit evidence.
