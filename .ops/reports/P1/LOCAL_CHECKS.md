# P1 local verification procedure

Executed as the ordinary development user from /home/codexperf/projects/gcreation-performance. Result: LOCAL_VALIDATION.txt; identities/counts: ARTIFACT_VERIFICATION.json. No privileged CLI or installed component was executed. No live health or scan request was made. These checks are LOCAL_TESTED only.

The Python standard-library verifier asserted:

- Effective UID is non-root; reviewed archive is a bounded regular, non-symlink project file.
- Archive SHA-256 equals the separately recorded human-approved V4 hash.
- Gzip expansion <=96 MiB; tar entries are unique regular safe paths, individual size <=8 MiB; no config.php, .env, node_modules or .git entry.
- Exactly 82 members; REVIEW_SOURCE_COMMIT matches the exact 40-character V4 source commit.
- All 81 other members equal that commit's Git blobs, using scripts/repo-git.sh show SOURCE:PATH.
- All 78 V4 manifest SHA-256 entries match the original archive (governance documents have since changed).
- Every archived ops/dev input and the seven dependency/trusted-policy influencing files match current workspace bytes: 30 files.
- Immutable prior validation log retains its recorded SHA-256; it was referenced, not duplicated or rerun.
- No .ops/deploy-dev.request exists, including dangling symlinks.
- Expected snapshot digest is SHA-256 of sorted UTF-8 relative path + NUL + binary SHA-256(content) for all 82 members. This is a locally expected digest, not an observed root/deployed snapshot.

## Exact targeted regression command

```sh
PYTHONPATH=tests python3 -m unittest -v test_security_review_v4.FourthReviewTests.test_builder_offline_frozen_dependencies_and_no_credentials test_security_review_v4.FourthReviewTests.test_artifact_hash_marker_and_snapshot_identity_are_bound test_security_review_v4.FourthReviewTests.test_dependency_manifest_changes_and_unsafe_archives_rejected test_security_review_v4.FourthReviewTests.test_request_requires_archive_hash_and_rejects_old_workspace_semantics test_security_review_v3.ThirdReviewTests.test_stale_regular_and_symlink_request_block_installation
```

All five tests passed. Fixtures/mocks run only under project-local .ops/test-artifacts and are cleaned up; the selected tests do not invoke Docker, root, systemd, Plesk, DNS or installed services. Prior comprehensive V4 checks are referenced at their source/handoff/hash; they are not relabeled as fresh P1 or live DEV results.
