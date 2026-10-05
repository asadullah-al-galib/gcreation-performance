# Acceptance evidence ledger

Authoritative scope: docs/MASTER_PRODUCT_SPEC.md, including all sections and named deliverables. Each DEV acceptance item requires direct current-state evidence. Local tests alone do not prove DEV deployment.

| ID  | Requirement                                                 | Status / evidence needed                             |
| --- | ----------------------------------------------------------- | ---------------------------------------------------- |
| D01 | public URL submission works                                 | Pending: observable DEV behavior plus relevant tests |
| D02 | dangerous/internal URLs are rejected                        | Pending: observable DEV behavior plus relevant tests |
| D03 | redirect SSRF protection is tested                          | Pending: observable DEV behavior plus relevant tests |
| D04 | jobs persist                                                | Pending: observable DEV behavior plus relevant tests |
| D05 | concurrency remains 1                                       | Pending: observable DEV behavior plus relevant tests |
| D06 | genuine progress is visible                                 | Pending: observable DEV behavior plus relevant tests |
| D07 | website discovery works                                     | Pending: observable DEV behavior plus relevant tests |
| D08 | sitemap discovery works                                     | Pending: observable DEV behavior plus relevant tests |
| D09 | homepage browser analysis works                             | Pending: observable DEV behavior plus relevant tests |
| D10 | product discovery works where applicable                    | Pending: observable DEV behavior plus relevant tests |
| D11 | Lighthouse metrics work                                     | Pending: observable DEV behavior plus relevant tests |
| D12 | normalized metrics persist                                  | Pending: observable DEV behavior plus relevant tests |
| D13 | deterministic rules create evidence-backed findings         | Pending: observable DEV behavior plus relevant tests |
| D14 | free report renders                                         | Pending: observable DEV behavior plus relevant tests |
| D15 | WordPress plugin works on DEV                               | Pending: observable DEV behavior plus relevant tests |
| D16 | trusted package/pricing selection works                     | Pending: observable DEV behavior plus relevant tests |
| D17 | WooCommerce DEV checkout works                              | Pending: observable DEV behavior plus relevant tests |
| D18 | paid audit creation is idempotent                           | Pending: observable DEV behavior plus relevant tests |
| D19 | secure paid-report foundation works                         | Pending: observable DEV behavior plus relevant tests |
| D20 | Interactive Fix Center works                                | Pending: observable DEV behavior plus relevant tests |
| D21 | expert request works                                        | Pending: observable DEV behavior plus relevant tests |
| D22 | first-100 analytics are recorded                            | Pending: observable DEV behavior plus relevant tests |
| D23 | critical automated tests pass                               | Pending: observable DEV behavior plus relevant tests |
| D24 | DEV deployment succeeds                                     | Pending: observable DEV behavior plus relevant tests |
| D25 | internal health succeeds                                    | Pending: observable DEV behavior plus relevant tests |
| D26 | public /perf-engine/health succeeds after human proxy setup | Pending: observable DEV behavior plus relevant tests |
| D27 | runtime resource limits are active                          | Pending: observable DEV behavior plus relevant tests |
| D28 | browser concurrency remains bounded                         | Pending: observable DEV behavior plus relevant tests |
| D29 | production was never touched                                | Pending: observable DEV behavior plus relevant tests |
| D30 | develop is committed and pushed                             | Pending: observable DEV behavior plus relevant tests |
| D31 | MASTER_EXEC_PLAN accurately reflects final state            | Pending: observable DEV behavior plus relevant tests |

Required artifacts: root docs, module directories, all six named DEV kit files, .ops/ACTION_REQUIRED.md, package-lock.json and six npm quality commands. Tests must cover the unit/integration/security/E2E scopes in §43.
