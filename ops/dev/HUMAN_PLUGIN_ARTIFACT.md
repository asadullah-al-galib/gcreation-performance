# Separate human-approved WordPress artifact — review only

HOLD. This is a proposed future procedure, not permission or an instruction to deploy now. Autonomous WordPress deployment is disabled while DEV shares the Plesk subscription/PHP user. The runtime watcher never writes the Plesk filesystem and does not invoke PHP or this installer.

A human must separately approve the exact Git commit, deterministic source archive hash and the three plugin file hashes in the review manifest. The trust transition in ROOT_TRUST_TRANSITION.md produces the root-owned reviewed snapshot. Human approval for the Node runtime does not automatically approve PHP deployment. A new plugin version requires a new explicit artifact review.

After separate future approval, the human verifies the DEV FPM/PHP pool user in Plesk and verifies that `/var/www/vhosts/gcreation.agency/dev.gcreation.agency/wp-config.php` is owned by that same named non-root user. No production path or destination argument is accepted. The future command is:

```sh
/usr/bin/python3 -I "/var/lib/gcreation-perf-review/$COMMIT/snapshot/ops/dev/install-reviewed-plugin.py" "/var/lib/gcreation-perf-review/$COMMIT/snapshot" "$APPROVED_SHA" "$COMMIT" 'HUMAN_VERIFIED_DEV_PHP_OWNER'
```

The reviewed helper verifies the archive, complete snapshot identity/ownership/hash map, fixed DEV path components, approved PHP owner and the exact three source files. It reads reviewed plugin bytes and the root-only secret into memory. Before any WordPress write it forks, clears supplementary groups and drops to that approved PHP UID/GID. WordPress operations use anchored directory descriptors without following path symlinks; only the fixed plugin is staged/replaced. Root never writes agent-controlled PHP into WordPress. A lock serializes human artifact operations; previous plugin content is renamed to one backup and restored if replacement fails. The human handles activation and verifies site health/readability after the separate artifact step; no WordPress code is executed by this helper.

Generated `config.php` is **0600**, owned by the verified DEV PHP UID. That UID must be the actual PHP/FPM reader. No shared-group read permission is granted. Public JS/CSS and the plugin entry file are 0644 with a 0755 plugin directory. Local ordinary-user tests verify the secret file owner can read the bytes, its mode is 0600, and group/other permission bits are zero; actual DEV PHP readability requires future human validation. A mode change to 0640 is not an accepted fallback.

Browser → WordPress nonce/session REST → WordPress PHP → `http://127.0.0.1:3101` with the server-held secret. Browsers never receive ENGINE_SECRET. Public nginx exposes only GET health; all engine business/admin routes remain localhost-only. Do not include the runtime environment, generated config.php, report tokens or customer data in review artifacts.
