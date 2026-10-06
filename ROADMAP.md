# Roadmap

[PROJECT_TIMELINE.md](PROJECT_TIMELINE.md) is the single authoritative MVP v0.1 execution order. Original M0.1–M0.32 intent remains verbatim in docs/MASTER_PRODUCT_SPEC.md §48 and is individually mapped in the timeline. This file is only an index, not a second plan.

| Part | Fixed purpose                              | Original milestone ownership                 | Current state                                                    |
| ---- | ------------------------------------------ | -------------------------------------------- | ---------------------------------------------------------------- |
| P0   | Governance Freeze                          | M0.1–M0.4                                    | FROZEN; human review PASS                                        |
| P1   | Security & DEV Deployment Foundation       | M0.5–M0.7                                    | HUMAN_CAPABILITY_GATE; REPAIR_1 source PASS; full review PENDING |
| P2   | Audit Engine Live Validation               | M0.8–M0.18                                   | NOT_STARTED; implementation largely present                      |
| P3   | WordPress Customer Flow                    | M0.19–M0.24                                  | NOT_STARTED; implementation largely present                      |
| P4   | Paid Service Flow                          | M0.25–M0.30                                  | NOT_STARTED; implementation largely present                      |
| P5   | Final Security / E2E / Resource Acceptance | M0.31                                        | NOT_STARTED                                                      |
| P6   | DEV Release Candidate                      | M0.32                                        | NOT_STARTED                                                      |
| P7   | First 100 Customer Validation              | Consumes M0.30 evidence; no new M0 milestone | NOT_STARTED                                                      |

P0 human review PASS: approved governance commit 1c6303e0c17b04952ee6e9c8b01d6868e53fe152. Accepted installation source08b395c independent security review PASS; REPAIR_1 source/security review PASS; full P1 review PENDING. Next allowed action: already-authorized operator controller refresh per .ops/reports/P1/TRUSTED_CONTROLLER_REFRESH_GATE.md; no request before verified refresh. V4 static security review: PASS. Installation gate: PASS by human-attested real-host evidence; single runtime deployment FAILED at non-root-build; its authorization is consumed; REPAIR_1 source/security review PASS; P0.2 grants controller refresh and conditional cycle-bound deployment; current refresh capability is unavailable. Real deployment/runtime/E2E acceptance remains pending. Production is untouched. Bounded sequential execution follows docs/P0_2_AUTONOMOUS_AUTHORIZATION.md; oversight PENDING does not block, defined capability/security stops do, P7/production remain forbidden. Do not add top-level Parts without human approval.

MVP SCOPE FREEZE and the two-repair limit are defined in PROJECT_TIMELINE.md and enforced by AGENTS.md. First 100 data informs future priorities; it does not authorize new infrastructure/features or production work.
