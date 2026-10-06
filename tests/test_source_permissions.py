"""Ordinary-user UMask=0077 fixtures; no controller entrypoint or host actions."""
import ast
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tarfile
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('permission_controller', str(ROOT / 'ops/dev/deploy_controller.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


class SourcePermissionTests(unittest.TestCase):
    def setUp(self):
        self.assertNotEqual(os.geteuid(), 0, 'Ordinary-user fixtures only')
        base = ROOT / '.ops/test-artifacts'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base))
        self.root = Path(self.temp.name)
        self.state = self.root / 'state'
        self.state.mkdir(mode=0o700)
        self.ops = self.root / 'ops'
        (self.ops / 'source-artifacts').mkdir(parents=True)
        self.trusted = self.root / 'trusted'
        self.trusted.mkdir()
        self.contents = {
            'REVIEW_SOURCE_COMMIT': ('a' * 40 + '\n').encode(),
            'package.json': b'{}', 'package-lock.json': b'{}',
            'apps/audit-service/src/main.ts': b'fixture app',
            'packages/scanner/src/proxy.ts': b'fixture proxy',
            'ops/dev/trusted/gateway.mjs': b'fixture gateway',
            'tests/deep/nested/fixture.txt': b'fixture test',
        }
        artifact = self.ops / 'source-artifacts' / ('a' * 40 + '.tar.gz')
        with tarfile.open(str(artifact), 'w:gz') as archive:
            for name, content in self.contents.items():
                member = tarfile.TarInfo(name)
                member.size = len(content)
                archive.addfile(member, io.BytesIO(content))
        self.request = {'action': 'deploy', 'commit': 'a' * 40,
                        'archive_sha256': hashlib.sha256(artifact.read_bytes()).hexdigest()}
        (self.trusted / 'dependency-baseline.json').write_text(json.dumps({
            name: hashlib.sha256(b'{}').hexdigest()
            for name in ('package.json', 'package-lock.json')}))

    def tearDown(self):
        self.temp.cleanup()  # Only this ordinary-user fixture, never host evidence.

    def create_source_roots(self):
        # Replay only actual release/source creation statements from deploy().
        # No root guard bypass, request claim, chown, subprocess or deploy() call.
        tree = ast.parse((ROOT / 'ops/dev/deploy_controller.py').read_text())
        deploy = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
                      and node.name == 'deploy')
        attempt = next(node for node in deploy.body if isinstance(node, ast.Try))
        def assigns(node, name):
            return (isinstance(node, ast.Assign) and
                    any(isinstance(target, ast.Name) and target.id == name
                        for target in node.targets))
        start = next(index for index, node in enumerate(attempt.body) if assigns(node, 'release'))
        end = next(index for index, node in enumerate(attempt.body) if assigns(node, 'digest'))
        module = ast.parse('')
        module.body = attempt.body[start:end]
        namespace = dict(controller.__dict__, STATE=self.state)
        exec(compile(ast.fix_missing_locations(module), 'source-root-fixture', 'exec'), namespace)
        return namespace['release'], namespace['snapshot']

    def extract(self, snapshot, request=None):
        fd = controller.open_directory(self.ops)
        try:
            with mock.patch.object(controller, 'TRUSTED', self.trusted):
                return controller.artifact_snapshot(fd, request or self.request, snapshot)
        finally:
            os.close(fd)

    def test_private_umask_source_roots_nested_directories_and_files_are_builder_readable(self):
        previous = os.umask(0o077)
        try:
            release, snapshot = self.create_source_roots()
            digest = self.extract(snapshot)
            self.assertEqual(digest, controller.snapshot_digest(snapshot))
            for path in [release, snapshot] + sorted(snapshot.rglob('*')):
                info = path.stat()
                self.assertEqual((info.st_uid, info.st_gid), (os.getuid(), os.getgid()))
                mode = stat.S_IMODE(info.st_mode)
                self.assertEqual(mode, 0o755 if path.is_dir() else 0o644, str(path))
                self.assertFalse(mode & 0o022, str(path))
                # Model a different UID/GID, such as the UID10001 builder
                # reading a root-owned bind mount: other r/x are required.
                self.assertEqual(mode & 0o005, 0o005 if path.is_dir() else 0o004)
            for name, content in self.contents.items():
                self.assertEqual((snapshot / name).read_bytes(), content)
            self.assertEqual(stat.S_IMODE(self.state.stat().st_mode), 0o700)
            observed = os.umask(0o077)
            self.assertEqual(observed, 0o077, 'Repair must not change process UMask')
        finally:
            os.umask(previous)

    def test_archive_and_dependency_verification_remain_fail_closed(self):
        previous = os.umask(0o077)
        try:
            _, snapshot = self.create_source_roots()
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                self.extract(snapshot, dict(self.request, archive_sha256='0' * 64))
            self.assertFalse(list(snapshot.iterdir()))
            (self.trusted / 'dependency-baseline.json').write_text(json.dumps({
                'package.json': '0' * 64, 'package-lock.json': '0' * 64}))
            with self.assertRaisesRegex(ValueError, 'Dependency manifest'):
                self.extract(snapshot)
        finally:
            os.umask(previous)

    def test_builder_identity_isolation_and_limits_remain_exact(self):
        with mock.patch.object(controller, 'runtime_image', return_value='sha256:' + 'e' * 64):
            args = controller.build_command(Path('/fixture/source'), Path('/fixture/output'))
        expected = ['docker', 'run', '--rm', '--name', 'gcreation-perf-dev-build', '--network=none',
                    '--user', '10001:10001', '--cap-drop=ALL', '--security-opt=no-new-privileges',
                    '--security-opt=seccomp=/usr/local/lib/gcreation-perf-dev/seccomp_profile.json',
                    '--pids-limit=192', '--cpus=3.5', '--memory=1500m', '--memory-swap=1500m',
                    '--cgroup-parent=gcreation-perf-dev.slice', '--log-driver=local',
                    '--log-opt=max-size=5m', '--log-opt=max-file=2', '--init', '--read-only',
                    '--mount=type=bind,src=/fixture/source,dst=/source,readonly',
                    '--mount=type=bind,src=/fixture/output,dst=/app', '--tmpfs=/tmp:rw,nosuid,size=128m',
                    'sha256:' + 'e' * 64, '/bin/sh', '-ec',
                    'cp -R /source/. /app/; ln -s /opt/gcreation-deps/node_modules /app/node_modules; '
                    'npm run format:check; npm run lint:ts; npm run typecheck; npm test; npm run build']
        self.assertEqual(args, expected)
        self.assertIn('UMask=0077', (ROOT / 'ops/dev/gcreation-perf-dev-deploy.service').read_text())


if __name__ == '__main__':
    unittest.main()
