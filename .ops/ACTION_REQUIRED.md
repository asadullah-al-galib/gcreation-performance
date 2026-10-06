STATUS:
P1 WAITING_FOR_HUMAN — FRESH-STAGE OPERATOR GATE

INDEPENDENT SECURITY REPAIR REVIEW: PASS for source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b, granted explicitly by the human. Accepted scope: only the demonstrated prepare_image import-bytecode defect repaired with two -I -B starts. V4 frozen boundaries remain accepted. Source PASS does not accept the contaminated old snapshot, installation/recovery, runtime, P2 or production.

P0 FROZEN / human PASS preserved. P1 execution IN_PROGRESS / full-Part independent review PENDING / repair_cycle0. P2–P7 NOT_STARTED. No gate wait consumes a repair.

ACTION FILE: [reports/P1/FRESH_STAGE_OPERATOR_GATE.md](reports/P1/FRESH_STAGE_OPERATOR_GATE.md).
APPROVAL RECORD: [reports/P1/SECURITY_REPAIR_ACCEPTANCE.json](reports/P1/SECURITY_REPAIR_ACCEPTANCE.json).

PROPOSED ARCHIVE SHA256: 80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929. Operator must verify the exact DATA/root-owned copy and separately approve fresh-stage recovery. Use source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b, never the current metadata commit as installation source.

NEXT ALLOWED ACTION: Explicit human/operator approval and fresh root-stage recovery per the gate. STOP. Preserve failed old root stage 8217aa4a13c0265efd8cb81473dd7f00c68d2c34 unchanged; do not reuse/clean/reapprove its snapshot or erase partial copied-install evidence. Like-for-like installed files/units remain until a separately approved human procedure. Old installation instructions are superseded.

PRIVILEGED DEV INSTALL: HOLD pending that separate operator decision/action. No agent privileged execution, partial-install modification, deployment request, runtime acceptance or P2 start. Production/main untouched. The accepted repair package remains unchanged historical review evidence at commit6c73ad3aa7e08df22fe552feb75da0b0a2122dc6.
