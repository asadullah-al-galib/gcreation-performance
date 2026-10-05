# Working plans

Use Inspect → Plan → Implement → Static Check → Test → Fix → Retest → Document → Commit → Push → Continue.

Keep original valid commits and DEV probe. Git metadata is read-only in the original .git; use isolated metadata inside this workspace, preserving remote develop history. Do not develop in /tmp under the current authorization.

Build the root kit as reviewable files, test its path/ownership/command boundaries without privilege, then continue all local engine/plugin tests. Request human installation once the concrete kit is ready. Deployed acceptance remains pending until actual DEV evidence exists.

MASTER_EXEC_PLAN.md is the changing execution ledger. REQUIREMENTS.md maps acceptance to evidence; docs/MASTER_PRODUCT_SPEC.md is the complete source of scope.
