# Roadmap

[PROJECT_TIMELINE.md](PROJECT_TIMELINE.md) is the single authoritative MVP v0.1 execution order. Original M0.1–M0.32 intent remains verbatim in docs/MASTER_PRODUCT_SPEC.md §48 and is individually mapped in the timeline. This file is only an index, not a second plan.

| Part | Fixed purpose                              | Original milestone ownership                 | Current state                                         |
| ---- | ------------------------------------------ | -------------------------------------------- | ----------------------------------------------------- |
| P0   | Governance Freeze                          | M0.1–M0.4                                    | FROZEN; human review PASS                               |
| P1   | Security & DEV Deployment Foundation       | M0.5–M0.7                                    | NOT_STARTED                                           |
| P2   | Audit Engine Live Validation               | M0.8–M0.18                                   | NOT_STARTED; implementation largely present           |
| P3   | WordPress Customer Flow                    | M0.19–M0.24                                  | NOT_STARTED; implementation largely present           |
| P4   | Paid Service Flow                          | M0.25–M0.30                                  | NOT_STARTED; implementation largely present           |
| P5   | Final Security / E2E / Resource Acceptance | M0.31                                        | NOT_STARTED                                           |
| P6   | DEV Release Candidate                      | M0.32                                        | NOT_STARTED                                           |
| P7   | First 100 Customer Validation              | Consumes M0.30 evidence; no new M0 milestone | NOT_STARTED                                           |

P0 human review PASS: approved governance commit 1c6303e0c17b04952ee6e9c8b01d6868e53fe152. Next allowed action: Explicit human start of P1. V4 static security review: PASS. Privileged DEV installation: HOLD pending explicit P1 human start. Real deployment/runtime/E2E acceptance remains pending. Production is untouched. No automatic next-Part execution: human PASS/FROZEN of the current Part and explicit next-Part start are mandatory. Do not add top-level Parts without human approval.

MVP SCOPE FREEZE and the two-repair limit are defined in PROJECT_TIMELINE.md and enforced by AGENTS.md. First 100 data informs future priorities; it does not authorize new infrastructure/features or production work.
