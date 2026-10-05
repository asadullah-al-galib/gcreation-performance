# Security contract

Only HTTP(S), public DNS/IP destinations, default HTTP(S) ports. Reject credentials, fragments, internal/single-label names, private/reserved/mapped IPv6, metadata and the audit host. Resolve every connection, pin the verified IP, and validate each redirect and browser resource. Browser service workers/downloads are disabled; proxy handles CONNECT to public port 443 only. Time, body, inventory, request and concurrency caps are mandatory.

Engine binds 127.0.0.1:3101. Management routes require a timing-safe secret comparison. Public /perf-engine/ proxies engine APIs/SSE; the engine requires its server-held secret for every route except health. Customer operations use the nonce/session-protected WordPress gateway. Never log request URLs containing report credentials. Report tokens are strong random values, hashed at rest; verification is rate limited and combines order/contact evidence. Mark-as-fixed is a claim, never verified success.

Privileged kit: fixed source/destination, no symlink/path substitution, snapshot reviewed source before non-root build, no repository code executed as root, lock, rollback, bounded releases, status file, preserve existing Plesk ownership. Root installs immutable trusted code; agents only create a request file. All runtime source executes as dedicated unprivileged users under externally enforced limits. No Docker socket/group granted to codexperf.

Release gate: automated SSRF tests, browser egress enforcement, runtime limits, payment idempotency, secure report tests and controlled public DEV E2E. Local mocks do not prove deployed behavior. Never touch production or unrelated customer sites.
