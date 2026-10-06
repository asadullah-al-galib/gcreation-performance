STATUS:
P1 WAITING_FOR_HUMAN — CONTROLLED DEV DEPLOYMENT + RUNTIME VALIDATION

INSTALLATION GATE: PASS — HUMAN_ATTESTED / REAL_DEV_VERIFIED installation only. Separately approved operator installation of source 08b395cf08523dbc5ab27f744d174b8a19bb2b4b / archive 80b206bf89d62f9a6b253970fea6a3a9cbe21b3106876e6e1e807df01a618929 completed with INSTALL_EXIT0. Observed root snapshot 867f258b5bb1261317caa6f601becbb4c7294569ff3b5bc4903d95f926f98fc3 exact; reviewed preflight PASS; no bytecode mutation; image sha256:f2bb2401f1f296115cd0d3dd5609ca6514446f55d4484f1884639f308a456f24 matches runtime-image-id; trusted files/units/dependency baseline match; ownership/private permissions attested. Watcher active/enabled, deploy service inactive, runtime containers/request absent. Old failed stage preserved unchanged.

EVIDENCE: [reports/P1/INSTALLATION_EVIDENCE.json](reports/P1/INSTALLATION_EVIDENCE.json). Observations supplied by the human; no agent host inspection. Individual numeric file hashes/host timestamps were not supplied and are not fabricated. The -I -B repair is now successfully validated for this installation defect on the real host, not for runtime acceptance.

ACTION FILE: [reports/P1/CONTROLLED_DEV_RUNTIME_GATE.md](reports/P1/CONTROLLED_DEV_RUNTIME_GATE.md).
NEXT ALLOWED ACTION: Human explicitly approves exactly ONE source-bound DEV deployment and bounded runtime/health/inspection scope with a designated ordinary-user submitter. No request/artifact/runtime action is performed by this gate preparation. No automatic retry, second deployment, fault, manual rollback or nginx/Plesk/WordPress change is included.

P0 FROZEN / human PASS; P1 execution IN_PROGRESS / full-Part independent review PENDING / repair_cycle0. P2–P7 NOT_STARTED. D24–D27 and runtime health/network/sandbox/cgroup/rollback/retention acceptance remain PENDING. A first deployment cannot prove rollback to a prior runtime when none exists; any missing proof requires a separate bounded human decision, not fabricated PASS or an extra request.

Source security review PASS and installation evidence are retained separately. Keep both root stages unchanged; do not reinstall or clean the old stage. No agent root/Docker/systemd/Plesk/nginx/WordPress action, deployment request, runtime continuation or P2 start. Production/main untouched. STOP at WAITING_FOR_HUMAN.
