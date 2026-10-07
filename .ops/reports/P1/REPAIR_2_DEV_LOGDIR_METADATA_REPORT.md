# P1 REPAIR_2 DEV log directory metadata analysis

The handoff SHA256 matches `bf791778f0fe31c4feec821d4535e71258455c25f88a0ed4bba9b38cf3fd73ac` and size 1622 bytes. All 34 lines, 25 global fields and 8 entry records (64 reported entry fields) are preserved. Evidence is operator supplied; Codex has not inspected the protected directory or opened any log contents.

The exact DEV directory `/var/www/vhosts/system/dev.gcreation.agency/logs` is reported existing, type directory and readable by the operator, mode 0700, UID980/GID0, mtime2026-10-06T21:43:17Z. Total8 entries, reported8, entry-limit truncation NO. All entries are regular files, mode0644, UID0/GID0, links2; no symlink target is reported. Global SYMLINK_FOLLOWED=NO is an operator attestation, not a separate per-entry measurement. Link count2 is compatible with hard links; aliases are unknown and were not resolved. No owner-name lookup, symlink following or other vhost access occurred.

| Basename | Conservative category | Bytes | Mtime UTC | Mode | UID:GID | Links | Window assessment |
| --- | --- | --- | --- | --- | --- | --- | --- |
| access_log | ACCESS_LOG_CANDIDATE | 0 | 2026-10-04T14:07:52Z | 0644 | 0:0 | 2 | LIKELY_TOO_OLD |
| access_log.processed | ROTATED_ACCESS_LOG_CANDIDATE | 9059 | 2026-10-06T21:29:31Z | 0644 | 0:0 | 2 | POTENTIALLY_COVERS_WINDOW |
| access_ssl_log | ACCESS_LOG_CANDIDATE | 13309 | 2026-10-07T06:48:34Z | 0644 | 0:0 | 2 | POTENTIALLY_COVERS_WINDOW |
| access_ssl_log.processed | ROTATED_ACCESS_LOG_CANDIDATE | 2859156 | 2026-10-06T21:29:31Z | 0644 | 0:0 | 2 | POTENTIALLY_COVERS_WINDOW |
| error_log | ERROR_LOG_CANDIDATE | 184 | 2026-10-04T14:07:52Z | 0644 | 0:0 | 2 | LIKELY_TOO_OLD |
| proxy_access_log | ACCESS_LOG_CANDIDATE | 666 | 2026-10-07T04:03:05Z | 0644 | 0:0 | 2 | POTENTIALLY_COVERS_WINDOW |
| proxy_access_ssl_log | ACCESS_LOG_CANDIDATE | 42426 | 2026-10-07T06:51:19Z | 0644 | 0:0 | 2 | POTENTIALLY_COVERS_WINDOW |
| proxy_error_log | ERROR_LOG_CANDIDATE | 1033 | 2026-10-05T04:08:00Z | 0644 | 0:0 | 2 | LIKELY_TOO_OLD |

Layout class: MIXED, meaning regular access/error candidates with two `.processed` access equivalents. The processed suffix suggests retained/processed access data; neither the rotation mechanism nor its interval is established. Categories use specific access/error/SSL/proxy naming plus regular-file metadata, not merely the presence of the word log. Actual log destinations and HTTP contents remain unverified.

The prior zero-recognized-file reason is NOT_ESTABLISHED — metadata insufficient (caseF). The inventory is not empty, symlink-only or directories-only at this observation. It does not reconstruct directory state at the earlier extraction. Its recognition rules and per-file rejection observations are absent, so unexpected filename or processed-file exclusion cannot be asserted as the cause. Filename differences alone do not prove an extractor defect. Directory mode/readability does not establish the previous extractor's credentials or an access failure.

The historical window is `2026-10-06T13:31:34Z..2026-10-06T13:32:36Z`. Empty access_log cannot supply rows at inventory. Pre-window mtimes on access_log/error_log/proxy_error_log make them conservatively LIKELY_TOO_OLD, without proving original health. Nonempty post-window candidates POTENTIALLY_COVER the window: that means possible, not measured coverage. Mtime is not creation time, log start/end time or a retention range. No candidate is classified LIKELY_TOO_NEW solely from a later mtime. No content range, HTTP status, error row, GET / row or unique caller evidence has been supplied.

## One proposed file read — not authorized

Best candidate: `/var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log`. Type ACCESS, reported ENTRY_03, regular, 13309 bytes, UID0/GID0, mode0644, links2, mtime2026-10-07T06:48:34Z. Window assessment POTENTIALLY_COVERS_WINDOW; actual coverage NOT_PROVEN. Selection follows priority1: a nonempty regular DEV access candidate with SSL naming matching the HTTPS homepage predicate, before proxy/error/processed equivalents. This is a candidate inference, not proof that the watcher request reached this file. No second file is selected or requested.

PROPOSED_SINGLE_FILE_READ — NOT AUTHORIZED: one human/operator read-only extraction from /var/www/vhosts/system/dev.gcreation.agency/logs/access_ssl_log for 2026-10-06T13:31:34Z..2026-10-06T13:32:36Z, GET / only, maximum 64 rows/16 KiB; sanitize client IPs, headers, user agents, query strings, cookies, tokens, secrets and bodies. No symlink following, other file reads or runtime action.

This proposal requires separate human authorization for exactly this file. If later authorized, confirm it remains regular and the path has no symlink traversal; stop if identity/type changes. Output only sanitized GET / rows in the exact UTC window plus coverage/no-match/truncation limits, retaining UTC timestamp/status and categorical Python-urllib attribution when supported. Do not emit raw user agents, query strings, client details or bodies. No other file read, broad search, symlink following or runtime action. A no-match result with unknown coverage never proves localhost failure.

The prior extractor's UNAVAILABLE content coverage and zero reported Python-urllib requests remain historical findings with their limits. Metadata does not establish internal or homepage health. The accepted controller still checks localhost health identity/HTTP200 before HTTPS DEV homepage HTTP200 and discards each inner exception. The proven outer error remains `RuntimeError: Runtime readiness deadline exceeded`; root cause, failed predicate and underlying component remain NOT_ESTABLISHED.

State HARD_BLOCKED; P1 BLOCKED/full review PENDING; INITIAL failed/consumed, REPAIR_1 failed/consumed1/1 and REPAIR_2 failed/consumed1/1. repair_cycle2, failed repair cycles2, retries0, budget exhausted. P2–P7 NOT_STARTED; production/main untouched. No source repair, exception repair, REPAIR_3, deployment request, budget extension/reset, protected content read, runtime action or mutation is authorized or performed. Any future repair/deployment requires NEW explicit human repair-budget authorization and applicable security review.

Evidence: `.ops/reports/P1/REPAIR_2_DEV_LOGDIR_METADATA_OPERATOR_HANDOFF.txt` and `.ops/reports/P1/REPAIR_2_DEV_LOGDIR_METADATA_ANALYSIS.json`. All prior failure records, handoffs, reviews and oversight events are preserved unchanged.
