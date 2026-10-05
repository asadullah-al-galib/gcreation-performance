"""V3 regressions. No root, Docker, systemctl or Plesk execution."""
import ast
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tarfile
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / file))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


preflight = load('install_preflight', 'ops/dev/install_preflight.py')
controller = load('review_controller_v3', 'ops/dev/deploy_controller.py')
plugin = load('review_plugin_v3', 'ops/dev/install-reviewed-plugin.py')
exporter = load('review_export_v3', 'ops/dev/review_archive.py')


class ThirdReviewTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / '.ops/test-artifacts'; base.mkdir(exist_ok=True, parents=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base))
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def bootstrap(self, archive, approved, commit):
        # Execute the documented DATA-only stdin recipe as the current user.
        # Only its fixed staging location and ownership/UID observations are
        # redirected/mocked; no identity change or privileged host commands.
        doc = (ROOT / 'ops/dev/ROOT_TRUST_TRANSITION.md').read_text()
        source = doc.split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
        tree = ast.parse(source)
        test_root = self.root

        class RedirectStaging(ast.NodeTransformer):
            def visit_Str(self, node):
                if node.s == '/var/lib/gcreation-perf-review':
                    return ast.copy_location(ast.Str(s=str(test_root)), node)
                return node

        tree = ast.fix_missing_locations(RedirectStaging().visit(tree))
        original_lstat = Path.lstat

        def root_owned(path):
            data = list(original_lstat(path)); data[4] = 0; data[0] &= ~0o022
            return os.stat_result(data)

        with mock.patch.object(sys, 'argv', ['-', commit, approved]), \
                mock.patch.object(os, 'geteuid', return_value=0), \
                mock.patch.object(Path, 'lstat', root_owned):
            exec(compile(tree, 'reviewed-bootstrap-stdin', 'exec'), {})

    def archive_fixture(self, commit, unsafe=None):
        stage = self.root / commit; stage.mkdir()
        target = stage / 'reviewed-source.tar.gz'
        with tarfile.open(str(target), 'w:gz') as data:
            payload = (commit + '\n').encode()
            marker = tarfile.TarInfo('REVIEW_SOURCE_COMMIT'); marker.size = len(payload)
            data.addfile(marker, io.BytesIO(payload))
            member = tarfile.TarInfo(unsafe or 'ops/dev/safe.txt')
            if unsafe == 'symlink':
                member.type = tarfile.SYMTYPE; member.linkname = '/etc/shadow'
                data.addfile(member)
            else:
                member.size = 4; data.addfile(member, io.BytesIO(b'data'))
        target.chmod(0o600)
        return target, hashlib.sha256(target.read_bytes()).hexdigest()

    def test_root_staging_sha_mismatch_aborts_before_extraction(self):
        commit = 'a' * 40
        target, _ = self.archive_fixture(commit)
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            self.bootstrap(target, '0' * 64, commit)
        self.assertFalse((target.parent / 'snapshot').exists())

    def test_bootstrap_rejects_links_and_traversal_before_extraction(self):
        for index, unsafe in enumerate(['symlink', '../escape', '/absolute']):
            commit = str(index) * 40
            target, digest = self.archive_fixture(commit, unsafe)
            with self.assertRaisesRegex(ValueError, 'Unsafe archive entry'):
                self.bootstrap(target, digest, commit)
            self.assertFalse((target.parent / 'snapshot').exists())

    def test_bootstrap_extracts_only_data_and_records_exact_identity(self):
        commit = 'b' * 40
        target, digest = self.archive_fixture(commit)
        self.bootstrap(target, digest, commit)
        self.assertEqual((target.parent / 'snapshot/ops/dev/safe.txt').read_text(), 'data')
        record = target.parent / 'approved.json'
        self.assertEqual(record.stat().st_mode & 0o777, 0o600)
        metadata = json.loads(record.read_text())
        self.assertEqual(metadata['commit'], commit)
        self.assertEqual(metadata['archive_sha256'], digest)
        self.assertEqual(metadata['files']['ops/dev/safe.txt'], hashlib.sha256(b'data').hexdigest())

    def test_installer_inputs_are_root_snapshot_only_and_preflight_precedes_install(self):
        source = (ROOT / 'ops/dev/install-root.sh').read_text()
        self.assertNotIn('/home/codexperf', source)
        self.assertNotIn('--check-install-source', source)
        self.assertIn('/var/lib/gcreation-perf-review/$REVIEWED_COMMIT/snapshot', source)
        self.assertIn('$(stat -c %u', source)
        self.assertIn('8#$trusted_mode & 022', source)
        self.assertLess(source.index('/usr/bin/python3 -I "$KIT_DIR/install_preflight.py"'), source.index('install -d'))
        self.assertGreater(source.rindex('/usr/bin/python3 -I "$KIT_DIR/install_preflight.py"'), source.index('docker build'))
        self.assertLess(source.rindex('/usr/bin/python3 -I "$KIT_DIR/install_preflight.py"'), source.index('systemctl enable'))
        self.assertIn('/usr/bin/python3 -I - "$COMMIT" "$APPROVED_SHA"', (ROOT / 'ops/dev/ROOT_TRUST_TRANSITION.md').read_text())
        self.assertIn('/usr/bin/python3 -I ', (ROOT / 'ops/dev/deploy-dev.sh').read_text())
        with self.assertRaisesRegex(ValueError, 'fixed root-owned'):
            preflight.verify_snapshot(ROOT, 'a' * 64, 'b' * 40)

    def test_stale_regular_and_symlink_request_block_installation(self):
        source = self.root / 'source'; (source / '.ops').mkdir(parents=True)
        preflight.reject_stale_request(source)
        request = source / '.ops/deploy-dev.request'
        request.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            preflight.reject_stale_request(source)
        request.unlink(); request.symlink_to(self.root / 'missing')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            preflight.reject_stale_request(source)

    def test_request_is_atomically_claimed_and_next_request_is_not_deleted(self):
        request = self.root / 'deploy-dev.request'
        data = {'action': 'deploy', 'commit': 'a' * 40}
        request.write_text(json.dumps(data))
        fd = controller.open_directory(self.root)
        try:
            claimed, parsed = controller.claim_request(fd)
            self.assertEqual(parsed, data)
            self.assertFalse(request.exists())
            self.assertEqual((self.root / claimed).read_text(), json.dumps(data))
            request.write_text(json.dumps({'action': 'deploy', 'commit': 'b' * 40}))
            os.unlink(claimed, dir_fd=fd)
            self.assertEqual(json.loads(request.read_text())['commit'], 'b' * 40)
        finally:
            os.close(fd)

    def test_request_schema_rejects_executable_or_extra_inputs(self):
        fd = controller.open_directory(self.root)
        try:
            for value in [{'action': 'deploy', 'commit': 'a' * 40, 'command': 'anything'},
                          {'action': 'shell', 'commit': 'a' * 40}, [],
                          {'action': 'deploy', 'commit': 7}]:
                (self.root / 'deploy-dev.request').write_text(json.dumps(value))
                with self.assertRaises(ValueError):
                    controller.claim_request(fd)
                self.assertFalse(list(self.root.glob('deploy-dev.claimed-*')))
        finally:
            os.close(fd)

    def test_auto_watcher_has_no_wordpress_write_or_deploy_capability(self):
        source = (ROOT / 'ops/dev/deploy_controller.py').read_text()
        unit = (ROOT / 'ops/dev/gcreation-perf-dev-deploy.service').read_text()
        installer = (ROOT / 'ops/dev/install-root.sh').read_text()
        for forbidden in ['wp-content', '/var/www', 'install-reviewed-plugin', 'plugin-deploy', 'php-lint']:
            self.assertNotIn(forbidden, source)
            self.assertNotIn(forbidden, unit)
        self.assertNotIn('install-reviewed-plugin', installer)
        self.assertIn('ProtectSystem=strict', unit)

    def test_public_proxy_exposes_only_health_and_no_client_secret(self):
        source = (ROOT / 'ops/dev/nginx-dev.conf.example').read_text()
        self.assertIn('location = /perf-engine/health', source)
        self.assertEqual(source.count('proxy_pass '), 1)
        self.assertIn('proxy_pass http://127.0.0.1:3101/health;', source)
        self.assertIn('proxy_pass_request_headers off;', source)
        self.assertIn('if ($request_method != GET) { return 405; }', source)
        self.assertIn('return 404;', source)
        self.assertNotIn('X-Engine-Secret', source)
        self.assertNotIn('$http_x_engine_secret', source)

    def network(self):
        return {'Name': controller.NETWORK, 'Id': 'a' * 64, 'Internal': True,
                'Driver': 'bridge', 'Scope': 'local', 'Labels': {'gcreation.role': 'dev-audit'}}

    def test_network_configuration_and_persisted_identity_fail_closed(self):
        baseline = self.network()
        variants = [{'Internal': False}, {'Driver': 'overlay'}, {'Scope': 'swarm'},
                    {'Name': 'other'}, {'Id': 'bad'}, {'Labels': {}}]
        with mock.patch.object(controller, 'STATE', self.root), mock.patch.object(controller, 'command') as command:
            for change in variants:
                network = dict(baseline); network.update(change)
                with mock.patch.object(controller, 'docker_json', side_effect=[{'Name': controller.NETWORK}, network]):
                    with self.assertRaises(ValueError):
                        controller.ensure_internal_network()
            with mock.patch.object(controller, 'docker_json', side_effect=[{'Name': controller.NETWORK}, baseline]):
                controller.ensure_internal_network()
            self.assertEqual((self.root / 'network-id').read_text(), baseline['Id'])
            changed = dict(baseline); changed['Id'] = 'b' * 64
            with mock.patch.object(controller, 'docker_json', side_effect=[{'Name': controller.NETWORK}, changed]):
                with self.assertRaisesRegex(ValueError, 'identity changed'):
                    controller.ensure_internal_network()
            command.assert_not_called()

    def test_network_creation_failure_is_not_ignored(self):
        with mock.patch.object(controller, 'docker_json', return_value=None), \
                mock.patch.object(controller, 'command', side_effect=RuntimeError('create failed')) as command:
            with self.assertRaisesRegex(RuntimeError, 'create failed'):
                controller.ensure_internal_network()
            self.assertNotIn('allow_failure', command.call_args[1])

    def test_network_mismatch_prevents_starting_any_runtime_container(self):
        with mock.patch.object(controller, 'ensure_internal_network', side_effect=ValueError('unsafe network')), \
                mock.patch.object(controller, 'command') as command:
            with self.assertRaises(ValueError):
                controller.start_runtime(self.root)
            command.assert_not_called()

    def test_snapshot_hash_verifier_rejects_changed_reviewed_files(self):
        commit = 'c' * 40
        target, digest = self.archive_fixture(commit)
        self.bootstrap(target, digest, commit)
        snapshot = target.parent / 'snapshot'
        with mock.patch.object(preflight, 'REVIEW_ROOT', self.root), \
                mock.patch.object(preflight, 'require_root_owned'):
            preflight.verify_snapshot(snapshot, digest, commit)
            (snapshot / 'ops/dev/safe.txt').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'content mismatch'):
                preflight.verify_snapshot(snapshot, digest, commit)
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                preflight.verify_archive(target, '0' * 64)

    def test_stale_preflight_failure_prevents_docker_and_service_operations(self):
        with mock.patch.object(os, 'geteuid', return_value=0), \
                mock.patch.object(preflight, 'verify_snapshot'), \
                mock.patch.object(preflight, 'reject_stale_request', side_effect=ValueError('Stale trigger')), \
                mock.patch.object(preflight, 'output') as output:
            with self.assertRaisesRegex(ValueError, 'Stale'):
                preflight.preflight(self.root, 'a' * 64, 'b' * 40)
            output.assert_not_called()

    def test_secure_environment_rejects_missing_or_injectable_secret(self):
        target = self.root / 'runtime.env'
        with mock.patch.object(preflight, 'ENVIRONMENT', target), \
                mock.patch.object(preflight, 'require_root_owned'):
            target.write_text('ENGINE_SECRET=' + 'a' * 64 + '\nDENIED_IPS=8.8.8.8\n')
            self.assertEqual(preflight.secure_environment()['ENGINE_SECRET'], 'a' * 64)
            for data in ["ENGINE_SECRET=quotes'not-allowed\nDENIED_IPS=8.8.8.8\n",
                         'ENGINE_SECRET=' + 'a' * 64 + '\nDENIED_IPS=127.0.0.1\n',
                         'ENGINE_SECRET=' + 'a' * 64 + '\nNODE_OPTIONS=bad\nDENIED_IPS=8.8.8.8\n']:
                target.write_text(data)
                with self.assertRaises(ValueError):
                    preflight.secure_environment()

    def test_docker_and_systemd_preflight_capabilities_fail_closed(self):
        info = {'CgroupDriver': 'systemd', 'OSType': 'linux', 'NCPU': 24}
        responses = [json.dumps(info), 'systemd 239\n', '239\n']
        with mock.patch.object(os, 'geteuid', return_value=0), \
                mock.patch.object(preflight, 'verify_snapshot'), \
                mock.patch.object(preflight, 'reject_stale_request'), \
                mock.patch.object(preflight, 'secure_environment'), \
                mock.patch.object(preflight, 'require_root_owned'), \
                mock.patch.object(preflight.platform, 'machine', return_value='x86_64'):
            with mock.patch.object(preflight, 'output', side_effect=responses):
                preflight.preflight(self.root, 'a' * 64, 'b' * 40)
            for outputs in [[json.dumps(dict(info, CgroupDriver='cgroupfs'))],
                            [json.dumps(dict(info, NCPU=2))],
                            [json.dumps(info), 'systemd 238\n'],
                            [json.dumps(info), 'systemd 239\n', '']]:
                with mock.patch.object(preflight, 'output', side_effect=outputs):
                    with self.assertRaises(ValueError):
                        preflight.preflight(self.root, 'a' * 64, 'b' * 40)
            with mock.patch.object(preflight, 'output', side_effect=RuntimeError('daemon unavailable')):
                with self.assertRaises(RuntimeError):
                    preflight.preflight(self.root, 'a' * 64, 'b' * 40)

    def test_root_secret_file_permission_policy_rejects_shared_group_read(self):
        target = self.root / 'runtime.env'; target.write_text('private'); target.chmod(0o640)
        original = Path.lstat
        def root_owned(path):
            data = list(original(path)); data[4] = 0; data[0] &= ~0o022
            return os.stat_result(data)
        with mock.patch.object(Path, 'lstat', root_owned):
            with self.assertRaisesRegex(ValueError, '0600'):
                preflight.require_root_owned(target, regular=True, private=True)

    def test_snapshot_digest_distinguishes_filename_content_boundaries(self):
        first = self.root / 'first'; first.mkdir()
        second = self.root / 'second'; second.mkdir()
        (first / 'a').write_text('bc')
        (second / 'ab').write_text('c')
        self.assertNotEqual(controller.snapshot_digest(first), controller.snapshot_digest(second))

    def test_plugin_secret_is_0600_owned_and_readable_by_writer_only(self):
        parent = plugin.open_directory(self.root)
        try:
            payload = {name: b'reviewed plugin bytes' for name in plugin.FILES}
            plugin.install_payload(parent, payload, 'a' * 64)
            config = self.root / 'gcreation-performance/config.php'
            self.assertEqual(config.stat().st_mode & 0o777, 0o600)
            self.assertEqual(config.stat().st_uid, os.getuid())
            self.assertIn('a' * 64, config.read_text())
            plugin.install_payload(parent, {name: b'new reviewed bytes' for name in plugin.FILES}, 'b' * 64)
            self.assertIn('a' * 64, (self.root / '.gcreation-performance-human-backup/config.php').read_text())
            self.assertIn('b' * 64, config.read_text())
        finally:
            os.close(parent)
        source = (ROOT / 'ops/dev/install-reviewed-plugin.py').read_text()
        self.assertLess(source.index('os.setuid(site.pw_uid)'), source.index("install_payload(parent, payload, environment['ENGINE_SECRET'])"))
        with mock.patch.object(os, 'geteuid', return_value=0):
            with self.assertRaises(PermissionError):
                plugin.install_payload(-1, {}, '')

    def test_base_images_are_digest_pinned_and_match_recorded_verification(self):
        record = json.loads((ROOT / 'ops/dev/BASE_IMAGE_DIGESTS.json').read_text())
        lines = [line for line in (ROOT / 'ops/dev/runtime.Dockerfile').read_text().splitlines() if line.startswith('FROM ')]
        self.assertEqual(len(lines), 2)
        for line, image in zip(lines, record['images']):
            self.assertIn(image['image'] + ':' + image['tag'] + '@' + image['digest'], line)
            self.assertRegex(line, r'@sha256:[0-9a-f]{64}( AS node)?$')
            self.assertNotIn('latest', line)

    def test_git_archive_export_is_deterministic_and_refuses_root(self):
        commit = 'a' * 40
        first = self.root / 'first.tar.gz'; second = self.root / 'second.tar.gz'
        def git_data(args):
            if '-t' in args:
                return b'commit\n'
            if 'ls-tree' in args:
                return ('100644 blob ' + 'b' * 40 + '\tmodule.ts\0').encode()
            self.assertIn('cat-file', args)
            return b'export const observed = true;\n'
        with mock.patch.object(exporter.subprocess, 'check_output', side_effect=git_data):
            self.assertEqual(exporter.export_archive(commit, first), exporter.export_archive(commit, second))
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with tarfile.open(str(first), 'r:gz') as data:
            self.assertTrue(all(member.isreg() for member in data))
            self.assertEqual(data.extractfile('REVIEW_SOURCE_COMMIT').read(), (commit + '\n').encode())
        with mock.patch.object(os, 'geteuid', return_value=0):
            with self.assertRaises(PermissionError):
                exporter.export_archive(commit, self.root / 'root.tar.gz')


if __name__ == '__main__':
    unittest.main()
