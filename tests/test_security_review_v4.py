"""V4 trust/network/artifact regressions; ordinary UID, fixture DATA and mocks only."""
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]

def load(name, file):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / file))
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

controller = load('v4_controller', 'ops/dev/deploy_controller.py')
preflight = load('v4_preflight', 'ops/dev/install_preflight.py')
image = load('v4_image', 'ops/dev/prepare_image.py')


class FourthReviewTests(unittest.TestCase):
    def setUp(self):
        base = ROOT / '.ops/test-artifacts'; base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base)); self.root = Path(self.temp.name)
        self.state = self.root / 'state'; self.state.mkdir()
        self.trusted = self.root / 'trusted'; self.trusted.mkdir()
        (self.trusted / 'runtime-image-id').write_text('sha256:' + 'e' * 64)

    def tearDown(self):
        self.temp.cleanup()

    def test_trusted_containers_never_mount_mutable_source_or_receive_master_proxy_secret(self):
        with mock.patch.multiple(controller, STATE=self.state, TRUSTED=self.trusted), \
                mock.patch.object(controller, 'ensure_internal_network'), \
                mock.patch.object(controller, 'ensure_egress_network'), \
                mock.patch.object(controller, 'ensure_host_access_network'), \
                mock.patch.object(controller, 'health'), \
                mock.patch.object(controller, 'command') as command:
            controller.start_runtime(self.root / 'malicious-release')
        runs = {call[0][0][call[0][0].index('--name') + 1]: call[0][0] for call in command.call_args_list if call[0][0][1] == 'run'}
        for name in (controller.PROXY, controller.GATEWAY):
            args = runs[name]
            self.assertFalse(any(arg.startswith('--mount') for arg in args))
            self.assertTrue(args[-1].startswith('/opt/gcreation-trusted/'))
            self.assertNotIn('ENGINE_SECRET', ' '.join(args))
            self.assertNotIn('--network=bridge', args)
            self.assertIn('sha256:' + 'e' * 64, args)
        self.assertIn('--env-file=' + str(self.state / 'proxy.env'), runs[controller.PROXY])
        self.assertNotIn('-p', runs[controller.APP])
        self.assertNotIn('-p', runs[controller.GATEWAY])
        self.assertIn(['docker', 'network', 'connect', '--ip', '172.31.255.2', controller.HOST_ACCESS_NETWORK, controller.GATEWAY], [call[0][0] for call in command.call_args_list])
        self.assertIn(['docker', 'network', 'connect', controller.EGRESS, controller.PROXY], [call[0][0] for call in command.call_args_list])
        self.assertNotIn('bridge', [arg for call in command.call_args_list for arg in call[0][0]])

    def test_builder_offline_frozen_dependencies_and_no_credentials(self):
        with mock.patch.object(controller, 'TRUSTED', self.trusted):
            args = controller.build_command(self.root / 'source', self.root / 'output')
        self.assertIn('--network=none', args)
        self.assertIn('--read-only', args)
        self.assertNotIn('npm ci', args[-1])
        self.assertIn('/opt/gcreation-deps/node_modules', args[-1])
        self.assertNotIn('--env-file', ' '.join(args))
        for gate in ['format:check', 'lint:ts', 'typecheck', 'npm test', 'npm run build']:
            self.assertIn(gate, args[-1])

    def test_reviewed_image_copies_only_fixed_snapshot_files_and_freezes_hashes(self):
        snapshot = self.root / 'reviewed'; snapshot.mkdir()
        for name in image.FILES + ['ops/dev/runtime.Dockerfile']:
            target = snapshot / name; target.parent.mkdir(parents=True, exist_ok=True); target.write_text('reviewed ' + name)
        with mock.patch.object(image, 'DEST', self.trusted):
            image.prepare(snapshot)
        frozen = self.trusted / 'build-context/trusted-source/packages/scanner/src/proxy.ts'
        (snapshot / 'packages/scanner/src/proxy.ts').write_text('later mutable edit')
        self.assertEqual(frozen.read_text(), 'reviewed packages/scanner/src/proxy.ts')
        baseline = json.loads((self.trusted / 'dependency-baseline.json').read_text())
        self.assertEqual(baseline['package.json'], hashlib.sha256(b'reviewed package.json').hexdigest())
        dockerfile = (ROOT / 'ops/dev/runtime.Dockerfile').read_text()
        self.assertIn('npm ci --ignore-scripts', dockerfile)
        self.assertIn('RUN --network=none', dockerfile)
        self.assertLess(dockerfile.index('npm ci'), dockerfile.index('COPY trusted-source/'))

    def network(self):
        return {'Name': controller.EGRESS, 'Id': 'a' * 64, 'Internal': False, 'Driver': 'bridge', 'Scope': 'local', 'Labels': {'gcreation.role': 'dev-audit-egress'}, 'Containers': {}}

    def test_egress_identity_configuration_and_unrelated_members_fail_closed(self):
        baseline = self.network()
        changes = [{'Internal': True}, {'Name': 'bridge'}, {'Driver': 'overlay'}, {'Scope': 'swarm'}, {'Labels': {}}, {'Labels': {'gcreation.role': 'dev-audit-egress', 'other': 'bad'}}, {'Containers': {'b' * 64: {'Name': 'unrelated'}}}, {'Containers': {'b' * 64: {'Name': controller.APP}}}]
        with mock.patch.multiple(controller, STATE=self.state, TRUSTED=self.trusted), mock.patch.object(controller, 'command') as command:
            for change in changes:
                with mock.patch.object(controller, 'docker_json', side_effect=[{'Name': controller.EGRESS}, dict(baseline, **change)]):
                    with self.assertRaises(ValueError): controller.ensure_egress_network()
            with mock.patch.object(controller, 'docker_json', side_effect=[{}, baseline]): controller.ensure_egress_network()
            changed = dict(baseline, Id='c' * 64)
            with mock.patch.object(controller, 'docker_json', side_effect=[{}, changed]):
                with self.assertRaisesRegex(ValueError, 'identity changed'): controller.ensure_egress_network()
            command.assert_not_called()

    def test_named_member_cannot_impersonate_reviewed_proxy_or_add_default_bridge(self):
        network = dict(self.network(), Containers={'b' * 64: {'Name': controller.PROXY}})
        container = {'Id': 'b' * 64, 'Name': '/' + controller.PROXY, 'Image': 'sha256:' + 'e' * 64, 'Config': {'Labels': {'gcreation.role': 'proxy'}}, 'NetworkSettings': {'Networks': {controller.NETWORK: {'NetworkID': 'd' * 64}, controller.EGRESS: {'NetworkID': 'a' * 64}}}}
        with mock.patch.multiple(controller, STATE=self.state, TRUSTED=self.trusted):
            with mock.patch.object(controller, 'docker_json', side_effect=[{}, network, container]): controller.ensure_egress_network()
            for change in [dict(container, Image='mutable-tag'), dict(container, NetworkSettings={'Networks': dict(container['NetworkSettings']['Networks'], bridge={'NetworkID': 'f' * 64})})]:
                with mock.patch.object(controller, 'docker_json', side_effect=[{}, network, change]):
                    with self.assertRaises(ValueError): controller.ensure_egress_network()

    def test_secrets_have_distinct_exact_ownership_and_private_env_inputs(self):
        values = {'ENGINE_SECRET': 'a' * 64, 'APP_GATEWAY_SECRET': 'b' * 64, 'FETCH_PROXY_SECRET': 'c' * 64, 'DENIED_IPS': '103.112.63.86'}
        preflight.write_runtime_environments(values, self.state)
        expected = {'gateway.env': {'ENGINE_SECRET', 'APP_GATEWAY_SECRET'}, 'app.env': {'APP_GATEWAY_SECRET', 'FETCH_PROXY_SECRET', 'DENIED_IPS'}, 'proxy.env': {'FETCH_PROXY_SECRET', 'DENIED_IPS'}}
        for file, keys in expected.items():
            path = self.state / file
            self.assertEqual({line.split('=')[0] for line in path.read_text().splitlines()}, keys)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
        target = self.root / 'runtime.env'
        target.write_text('\n'.join(key + '=' + value for key, value in dict(values, FETCH_PROXY_SECRET='a' * 64).items()))
        with mock.patch.object(preflight, 'ENVIRONMENT', target), mock.patch.object(preflight, 'require_root_owned'):
            with self.assertRaisesRegex(ValueError, 'distinct'): preflight.secure_environment()

    def test_preflight_requires_raw_server_ip_and_every_public_dev_dns_answer(self):
        with mock.patch.object(preflight, 'resolve_dev_addresses', return_value=['103.112.63.86', '8.8.8.8']):
            for denied in ['8.8.8.8', '103.112.63.86', '1.1.1.1']:
                with self.assertRaisesRegex(ValueError, 'self-host'): preflight.verify_self_host_deny(denied)
            preflight.verify_self_host_deny('103.112.63.86,8.8.8.8')
        with mock.patch.object(preflight, 'resolve_dev_addresses', return_value=[]):
            with self.assertRaises(ValueError): preflight.verify_self_host_deny('103.112.63.86')

    def test_dev_dns_child_is_isolated_fixed_and_bounded(self):
        with mock.patch.object(preflight.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout=b'["103.112.63.86"]')) as run:
            self.assertEqual(preflight.resolve_dev_addresses(), ['103.112.63.86'])
        args = run.call_args[0][0]
        self.assertEqual(args[:3], ['/usr/bin/python3', '-I', '-c'])
        self.assertIn('dev.gcreation.agency', args[3])
        self.assertNotIn('performance.gcreation.agency', args[3])
        self.assertEqual(run.call_args[1]['timeout'], 10)
        self.assertEqual(set(run.call_args[1]['env']), {'PATH'})

    def artifact(self, extra=None, marker=None):
        artifacts = self.root / 'source-artifacts'; artifacts.mkdir(exist_ok=True)
        commit = 'a' * 40
        contents = {'REVIEW_SOURCE_COMMIT': ((marker or commit) + '\n').encode(), 'package.json': b'{}', 'package-lock.json': b'{}', 'packages/scanner/src/proxy.ts': b'mutable attacker proxy'}
        contents.update(extra or {})
        target = artifacts / (commit + '.tar.gz')
        with tarfile.open(str(target), 'w:gz') as archive:
            for name, content in contents.items():
                member = tarfile.TarInfo(name); member.size = len(content); archive.addfile(member, io.BytesIO(content))
        (self.trusted / 'dependency-baseline.json').write_text(json.dumps({name: hashlib.sha256(b'{}').hexdigest() for name in ('package.json', 'package-lock.json')}))
        return {'action': 'deploy', 'commit': commit, 'archive_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}

    def extract(self, request):
        snapshot = self.state / ('snapshot-' + str(len(list(self.state.iterdir())))); snapshot.mkdir()
        fd = controller.open_directory(self.root)
        try:
            with mock.patch.object(controller, 'TRUSTED', self.trusted), mock.patch.object(controller.pwd, 'getpwnam', return_value=mock.Mock(pw_uid=os.getuid())):
                return snapshot, controller.artifact_snapshot(fd, request, snapshot)
        finally: os.close(fd)

    def test_artifact_hash_marker_and_snapshot_identity_are_bound(self):
        request = self.artifact()
        snapshot, digest = self.extract(request)
        self.assertEqual(digest, controller.snapshot_digest(snapshot))
        # Current workspace edits have no influence on immutable artifact bytes.
        (self.root / 'package.json').write_text('uncommitted malicious manifest')
        _, again = self.extract(request); self.assertEqual(again, digest)
        with self.assertRaisesRegex(ValueError, 'SHA-256'): self.extract(dict(request, archive_sha256='0' * 64))
        request = self.artifact(marker='b' * 40)
        with self.assertRaisesRegex(ValueError, 'marker'): self.extract(request)

    def test_dependency_manifest_changes_and_unsafe_archives_rejected(self):
        for name in ('package.json', 'package-lock.json'):
            request = self.artifact({name: b'changed'})
            with self.assertRaisesRegex(ValueError, 'Dependency manifest'): self.extract(request)
        for name in ('../escape', '/absolute', 'config.php', 'node_modules/bad.js'):
            request = self.artifact({name: b'bad'})
            with self.assertRaisesRegex(ValueError, 'Unsafe'): self.extract(request)

    def test_source_artifact_links_special_files_and_symlink_inputs_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.FIFOTYPE):
            request = self.artifact()
            target = self.root / 'source-artifacts' / (request['commit'] + '.tar.gz')
            with tarfile.open(str(target), 'w:gz') as archive:
                member = tarfile.TarInfo('unsafe'); member.type = kind; member.linkname = '/etc/shadow'
                archive.addfile(member)
            request['archive_sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValueError, 'Unsafe'): self.extract(request)
        request = self.artifact()
        target = self.root / 'source-artifacts' / (request['commit'] + '.tar.gz')
        target.rename(target.with_suffix('.data')); target.symlink_to(target.with_suffix('.data'))
        with self.assertRaises(OSError): self.extract(request)

    def test_request_requires_archive_hash_and_rejects_old_workspace_semantics(self):
        (self.root / 'deploy-dev.request').write_text(json.dumps({'action': 'deploy', 'commit': 'a' * 40}))
        fd = controller.open_directory(self.root)
        try:
            with self.assertRaisesRegex(ValueError, 'fixed deployment'): controller.claim_request(fd)
        finally: os.close(fd)

    def test_clean_root_environment_precedes_interpreters(self):
        for file in ('ROOT_TRUST_TRANSITION.md', 'HUMAN_PLUGIN_ARTIFACT.md'):
            text = (ROOT / 'ops/dev' / file).read_text()
            for line in text.splitlines():
                if line.startswith('/usr/bin/python3') or line.startswith('/bin/bash'):
                    self.fail('Inherited root environment in ' + file)
            self.assertIn('/usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I', text)
        self.assertIn('exec /usr/bin/env -i', (ROOT / 'ops/dev/deploy-dev.sh').read_text())


if __name__ == '__main__': unittest.main()
