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

## Local evidence and remaining deployed proof

| Criteria     | Current local evidence                                                                                                                          | Still required                                                                                     |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| D01–D03      | foundation/security/API tests: parsing, DNS answers, private IPs, actual redirect policy and HTTP/CONNECT proxy socket rejection                | Controlled public submission and browser/Lighthouse redirect/subresource SSRF on DEV               |
| D04–D06, D28 | SQLite reopen/recovery, unique running-job index, concurrent worker/admission tests, genuine persisted SSE and UI event rendering               | Real queued browser jobs, one live Chromium job, progress in DEV UI, crash cleanup                 |
| D07–D10      | Controlled sitemap/index/product fixtures, truncation and representative selection tests                                                        | Real discovery/browser analysis on authorized public target                                        |
| D11–D13      | Scanner/Lighthouse adapter compiled; observed-only normalization and all 16 rule-family fixtures pass; metrics persist per page                 | Actual lab measurements, stored rows and matching findings on DEV                                  |
| D14–D17      | jsdom free-report UI/escaping, WP session helper, server pricing boundary tests and PHP commerce contract harness                               | Activated plugin, real WooCommerce cart/session/checkout and manual payment                        |
| D18–D21      | Unique paid-order/payment tests; strong token+order+contact checks; fixed claim, restricted/idempotent retest comparison and expert/admin tests | Paid browser audit, delivered secure link, Fix Center/customer expert request on DEV               |
| D22          | Typed events, analytics persistence/resource sampling, actual package-selection event separate from price lookup                                | Real first-100 counters and observed scanner cgroup usage                                          |
| D23          | 24 TypeScript tests, 11 Python boundary tests, PHP lint/commerce, format/lint/typecheck/build pass under pinned Node                             | Deployed/browser security and controlled E2E gates                                                 |
| D24–D27      | Root kit syntax/path/status/snapshot tests; fresh nonprivileged snapshot build; temporary loopback health 200                                   | Human installation, successful watched deploy, public/internal DEV health, effective resource caps |
| D29–D31      | Work remains project-local; prior history preserved; meaningful develop commits pushed; execution ledger maintained                             | Final full acceptance audit and final release commit/state                                         |

Exact deployed validation procedure: docs/DEV_VALIDATION_RUNBOOK.md. All broad DEV criteria above remain pending; no local mock is being used to assert deployed success.
