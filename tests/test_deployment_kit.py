"""Unprivileged boundary tests. No install, Docker or live filesystem mutations."""
import importlib.util
import json
import hashlib
import io
import tarfile
import sys
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('controller', str(ROOT / 'ops/dev/deploy_controller.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
preflight_spec = importlib.util.spec_from_file_location('install_preflight', str(ROOT / 'ops/dev/install_preflight.py'))
preflight = importlib.util.module_from_spec(preflight_spec)
sys.modules['install_preflight'] = preflight
preflight_spec.loader.exec_module(preflight)


class DeploymentBoundaryTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / '.ops/test-artifacts'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base))
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.fd = controller.open_directory(self.source)

    def tearDown(self):
        os.close(self.fd)
        self.temp.cleanup()

    def test_safe_snapshot_contents(self):
        (self.source / 'file').write_text('safe')
        controller.copy_entry(self.fd, 'file', self.root / 'copied', [0, 0])
        self.assertEqual((self.root / 'copied').read_text(), 'safe')

    def test_symlink_directory_and_file_rejected(self):
        (self.source / 'link').symlink_to('/etc/passwd')
        with self.assertRaises(ValueError):
            controller.copy_entry(self.fd, 'link', self.root / 'copied', [0, 0])
        (self.root / 'alias').symlink_to(self.source)
        with self.assertRaises(OSError):
            controller.open_directory(self.root / 'alias')
        with self.assertRaises(ValueError):
            controller.check_path(self.root / 'alias')

    def test_hardlink_special_and_traversal_rejected(self):
        (self.source / 'file').write_text('safe')
        os.link(str(self.source / 'file'), str(self.source / 'hard'))
        os.mkfifo(str(self.source / 'pipe'))
        for name in ['file', 'hard', 'pipe', '../file']:
            with self.assertRaises(ValueError):
                controller.copy_entry(self.fd, name, self.root / name.replace('/', '-'), [0, 0])

    def test_directory_fd_stays_anchored_on_path_swap(self):
        (self.source / 'file').write_text('original')
        self.source.rename(self.root / 'old')
        self.source.mkdir()
        (self.source / 'file').write_text('substitute')
        controller.copy_entry(self.fd, 'file', self.root / 'copied', [0, 0])
        self.assertEqual((self.root / 'copied').read_text(), 'original')

    def test_atomic_status_replaces_symlink_without_touching_target(self):
        outside = self.root / 'untouched'
        outside.write_text('original')
        (self.source / 'deploy-dev.status').symlink_to(outside)
        controller.status(self.fd, {'state': 'COMPLETED', 'commit': 'a' * 40})
        self.assertEqual(outside.read_text(), 'original')
        self.assertFalse((self.source / 'deploy-dev.status').is_symlink())
        self.assertIn('COMPLETED', (self.source / 'deploy-dev.status').read_text())

    def test_snapshot_excludes_local_credentials_and_caches(self):
        folder = self.source / 'module'
        folder.mkdir()
        (folder / '.env').write_text('test-secret')
        (folder / 'config.php').write_text('test-secret')
        (folder / 'code.ts').write_text('export const safe = true;')
        controller.copy_entry(self.fd, 'module', self.root / 'copied', [0, 0], exclude_private=True)
        self.assertEqual([file.name for file in (self.root / 'copied').iterdir()], ['code.ts'])

    def test_rollback_backup_preserves_plugin_configuration(self):
        folder = self.source / 'plugin'
        folder.mkdir()
        (folder / 'config.php').write_text('private-config-to-restore')
        (folder / 'config.php').chmod(0o640)
        controller.copy_entry(self.fd, 'plugin', self.root / 'backup', [0, 0])
        self.assertEqual((self.root / 'backup/config.php').read_text(), 'private-config-to-restore')
        self.assertEqual((self.root / 'backup/config.php').stat().st_mode & 0o777, 0o640)

    def test_privileged_runtime_contract(self):
        self.assertFalse(hasattr(controller, 'PLUGIN'))
        self.assertFalse(hasattr(controller, 'WP'))
        flags = controller.container_flags('1500m', '3.5')
        for flag in ['--cap-drop=ALL','--security-opt=no-new-privileges','--pids-limit=192','--cgroup-parent=gcreation-perf-dev.slice']:
            self.assertIn(flag, flags)
        source = (ROOT / 'ops/dev/deploy_controller.py').read_text()
        self.assertNotIn('shell=True', source)
        self.assertNotIn('docker.sock', source)
        self.assertIn("'127.0.0.1:3101:3101'", source)
        self.assertIn("'--internal'", source)

    def test_failed_release_retention_preserves_active_rollback_source(self):
        previous = controller.STATE
        controller.STATE = self.root
        try:
            for number in range(5):
                (self.root / ('release-' + str(number))).mkdir()
            controller.prune_releases({self.root / 'release-0', self.root / 'release-4'})
            self.assertEqual(sorted(path.name for path in self.root.glob('release-*')),
                             ['release-0', 'release-3', 'release-4'])
        finally:
            controller.STATE = previous

    def simulate_deployment(self, fail_health=False, next_request=False):
        # Simulate host operations; never invoke the installed controller, Docker,
        # Plesk PHP or privileged filesystem/ownership operations.
        wp = self.root / 'dev-wordpress'
        plugin = wp / 'wp-content/plugins/gcreation-performance'
        plugin.mkdir(parents=True)
        (plugin / 'old.php').write_text('previous-plugin')
        (plugin / 'config.php').write_text('previous-private-configuration')
        (plugin / 'config.php').chmod(0o600)
        expected_owner = (plugin.stat().st_uid, plugin.stat().st_gid)
        state = self.root / 'state'; state.mkdir()
        prior_release = state / 'release-0'; prior_release.mkdir()
        (state / 'active.json').write_text(json.dumps({'release': str(prior_release), 'commit': 'a' * 40}))
        trusted = self.root / 'trusted'; trusted.mkdir()
        ops = self.source / '.ops'; ops.mkdir()
        artifacts = ops / 'source-artifacts'; artifacts.mkdir()
        artifact = artifacts / ('b' * 40 + '.tar.gz')
        contents = {'REVIEW_SOURCE_COMMIT': ('b' * 40 + '\n').encode(), 'package.json': b'{}', 'package-lock.json': b'{}', 'wordpress/sentinel.php': b'<?php /* untrusted DATA */'}
        with tarfile.open(str(artifact), 'w:gz') as archive:
            for name, content in contents.items():
                member = tarfile.TarInfo(name); member.size = len(content)
                archive.addfile(member, io.BytesIO(content))
        digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
        (trusted / 'dependency-baseline.json').write_text(json.dumps({name: hashlib.sha256(contents[name]).hexdigest() for name in ('package.json', 'package-lock.json')}))
        (trusted / 'runtime-image-id').write_text('sha256:' + 'd' * 64)
        (ops / 'deploy-dev.request').write_text(json.dumps({'action': 'deploy', 'commit': 'b' * 40, 'archive_sha256': digest}))
        source_plugin = self.source / 'wordpress/gcreation-performance'
        source_plugin.mkdir(parents=True)
        (source_plugin / 'new.php').write_text('<?php /* new plugin */')
        original_read = Path.read_text

        def read_text(path, *args, **kwargs):
            if str(path) == '/etc/gcreation-perf-dev/runtime.env':
                return 'ENGINE_SECRET=' + 'c' * 64 + '\nAPP_GATEWAY_SECRET=' + 'd' * 64 + '\nFETCH_PROXY_SECRET=' + 'e' * 64 + '\nDENIED_IPS=103.112.63.86\n'
            return original_read(path, *args, **kwargs)

        def check_health():
            if fail_health:
                raise RuntimeError('controlled final health failure')

        submitted = []

        def host_command(*args, **kwargs):
            if next_request and not submitted:
                self.assertFalse((ops / 'deploy-dev.request').exists())
                self.assertTrue(list(ops.glob('deploy-dev.claimed-*')))
                (ops / 'deploy-dev.request').write_text(json.dumps({'action': 'deploy', 'commit': 'c' * 40, 'archive_sha256': 'd' * 64}))
                submitted.append(True)

        replacements = dict(SOURCE=self.source, STATE=state,
                            TRUSTED=trusted, ALLOW=['wordpress'])
        with mock.patch.multiple(controller, **replacements), \
                mock.patch.object(controller.os, 'geteuid', return_value=0), \
                mock.patch.object(controller.os, 'chown') as ownership, \
                mock.patch.object(controller.pwd, 'getpwnam', return_value=SimpleNamespace(pw_uid=os.getuid())), \
                mock.patch.object(Path, 'read_text', read_text), \
                mock.patch.object(controller, 'command', side_effect=host_command) as commands, \
                mock.patch.object(controller, 'start_runtime') as runtime, \
                mock.patch.object(controller, 'ensure_internal_network'), \
                mock.patch.object(controller, 'ensure_egress_network'), \
                mock.patch.object(preflight, 'require_root_owned'), \
                mock.patch.object(preflight, 'resolve_dev_addresses', return_value=['103.112.63.86']), \
                mock.patch.object(controller, 'health', side_effect=check_health):
            if fail_health:
                with self.assertRaisesRegex(RuntimeError, 'controlled final health failure'):
                    controller.deploy()
            else:
                controller.deploy()
        return plugin, state, ops, expected_owner, ownership, commands, runtime

    def test_simulated_runtime_deploy_never_changes_wordpress_and_records_source_digest(self):
        plugin, state, ops, _, _, commands, runtime = self.simulate_deployment()
        status = json.loads((ops / 'deploy-dev.status').read_text())
        self.assertEqual(status['state'], 'COMPLETED')
        self.assertEqual(status['commit'], 'b' * 40)
        self.assertEqual(len(status['snapshot_sha256']), 64)
        active = json.loads((state / 'active.json').read_text())
        artifact = ops / 'source-artifacts' / ('b' * 40 + '.tar.gz')
        self.assertEqual(status['archive_sha256'], hashlib.sha256(artifact.read_bytes()).hexdigest())
        self.assertEqual(active['archive_sha256'], status['archive_sha256'])
        self.assertFalse((plugin / 'new.php').exists())
        self.assertTrue((plugin / 'old.php').exists())
        self.assertEqual((plugin / 'config.php').stat().st_mode & 0o777, 0o600)
        self.assertEqual((plugin / 'config.php').read_text(), 'previous-private-configuration')
        self.assertFalse((state / 'plugin-backup').exists())
        self.assertFalse((ops / 'deploy-dev.request').exists())
        self.assertEqual(runtime.call_count, 1)
        self.assertTrue(commands.called)

    def test_simulated_health_failure_preserves_wordpress_and_restores_prior_runtime(self):
        plugin, state, ops, expected_owner, ownership, _, runtime = self.simulate_deployment(True)
        self.assertEqual((plugin / 'old.php').read_text(), 'previous-plugin')
        self.assertFalse((plugin / 'new.php').exists())
        self.assertEqual((plugin / 'config.php').read_text(), 'previous-private-configuration')
        self.assertEqual((plugin / 'config.php').stat().st_mode & 0o777, 0o600)
        self.assertFalse(any(str(plugin) in str(call) for call in ownership.call_args_list))
        self.assertEqual(runtime.call_args[0][0], state / 'release-0')
        self.assertEqual(runtime.call_count, 2)
        status = json.loads((ops / 'deploy-dev.status').read_text())
        self.assertEqual(status['state'], 'FAILED')
        self.assertEqual(status['stage'], 'final-health')
        self.assertTrue(status['rollback'])
        self.assertFalse((ops / 'deploy-dev.request').exists())
        self.assertEqual(json.loads((state / 'active.json').read_text())['commit'], 'a' * 40)

    def test_request_arriving_during_deployment_survives_claim_cleanup(self):
        _, _, ops, _, _, _, _ = self.simulate_deployment(next_request=True)
        self.assertEqual(json.loads((ops / 'deploy-dev.request').read_text())['commit'], 'c' * 40)
        self.assertFalse(list(ops.glob('deploy-dev.claimed-*')))


if __name__ == '__main__':
    unittest.main()
