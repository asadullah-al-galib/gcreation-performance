# POST_100 deferred features

Scope: documentation only under P0.2§13; no feature below is authorized for implementation today. First-100 evidence may justify a proposal; it does not itself change scope. Keep existing boundaries rather than add speculative abstraction.

| Feature | Why deferred | First-100 trigger for reconsideration | Current compatibility constraint |
| --- | --- | --- | --- |
| Paid LLM diagnosis | Deterministic MVP must work without paid AI. | Reviewed audits show repeated explanation gaps deterministic rules cannot cover. | Keep evidence separate from explanation; replaceable provider; no fabricated measurements or required paid runtime. |
| PostgreSQL persistence | SQLite fits the bounded DEV MVP. | Measured sustained lock/contention or capacity limits in real consenting usage. | Preserve existing data/API semantics and explicit migration/rollback compatibility. |
| Redis/BullMQ/distributed execution | Browser concurrency one and bounded jobs suffice. | Measured queue latency/reliability exceeds approved limits despite current bounded model. | Preserve job IDs, progress accuracy, concurrency/resource bounds and offline trusted runtime. |
| Object storage and additional report formats | Bounded local artifacts and Interactive Fix Center serve launch. | Measured retention/storage limits or repeated customer format demand. | Preserve token authorization, privacy, retention/cleanup and existing report schema. |
| WordPress Connector/Admin diagnosis | Public frontend diagnosis is the approved MVP. | Consenting first-100 customers repeatedly need evidence unavailable publicly. | Human-only reviewed PHP, separate credentials, no automatic live optimization or watcher PHP deployment. |
| Continuous monitoring, scale/multi-region, microservices, Kubernetes | No demonstrated first-100 requirement; speculative infrastructure is excluded. | Actual sustained demand/resource data supports a scoped proposal. | Preserve V4 sandbox/network/SSRF boundaries, dependency freeze and single-browser limits until explicitly changed. |
| Large account dashboards, new SaaS billing, extra customer features | Existing customer journey/pricing/manual-payment scope must be completed first. | Real conversion/support evidence identifies a specific missing capability. | Preserve customer/session ownership, BDT pricing, payment idempotency and current frontend/API contracts. |
| Production deployment | Outside P0.2 authority. | Successful DEV P6 UAT plus a separate explicit production decision. | Main/production untouched; no first-100 observation grants production access. |
