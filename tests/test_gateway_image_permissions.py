"""No root/Docker: exact packaging regression plus a read-only image probe.

Fixture ownership/import is the ordinary user, not real image acceptance.
The human image gate runs the probe as UID10001 against root-owned image bytes.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import stat
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
NODE = os.environ.get('GCREATION_TEST_NODE', str(
    ROOT / '.ops/toolchain/node_modules/node/bin/node'))
PROBE = ROOT / 'tests/gateway-image-permissions-probe.mjs'
GATEWAY_SHA = 'd9616a205b5f7a7e2d11779a2a98a1a5367ec76d992b2d3b8bb51e5a25343c4c'
DIRECTORIES = ('ops', 'ops/dev', 'ops/dev/trusted')
spec = importlib.util.spec_from_file_location(
    'gateway_permission_prepare', str(ROOT / 'ops/dev/prepare_image.py'))
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


def inventory(root):
    result = {}
    for path in [root] + sorted(root.rglob('*')):
        info = path.lstat()
        result[str(path.relative_to(root))] = (
            info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode),
            hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None)
    return result


class GatewayImagePermissionTests(unittest.TestCase):
    def setUp(self):
        self.assertNotEqual(os.geteuid(), 0, 'Ordinary-user fixtures only')
        base = ROOT / '.ops/test-artifacts'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base))
        self.base = Path(self.temp.name)
        self.dest = self.base / 'private-host-context'
        self.dest.mkdir(mode=0o700)
        previous = os.umask(0o077)
        try:
            with mock.patch.object(prepare, 'DEST', self.dest):
                prepare.prepare(ROOT)
            self.image = self.base / 'image-trusted'
            shutil.copytree(str(self.dest / 'build-context/trusted-source'), str(self.image))
            # WORKDIR is image-owned0755; COPY preserves nested source0700.
            self.image.chmod(0o755)
        finally:
            os.umask(previous)
        self.gateway = self.image / 'ops/dev/trusted/gateway.mjs'
        self.assertEqual(hashlib.sha256(self.gateway.read_bytes()).hexdigest(), GATEWAY_SHA)

    def tearDown(self):
        for name in DIRECTORIES:
            (self.image / name).chmod(0o700)
        self.temp.cleanup()  # Only this disposable ordinary-user fixture.

    def apply_packaging_step(self):
        dockerfile = (ROOT / 'ops/dev/runtime.Dockerfile').read_text()
        line = next(line for line in dockerfile.splitlines() if 'chmod' in line)
        command = shlex.split(line.strip()[3:-1].strip())
        self.assertEqual(command, ['chmod', '0755'] + list(DIRECTORIES))
        subprocess.check_call(command, cwd=str(self.image))

    def probe(self):
        program = ('import {verifyGatewayImage} from ' + json.dumps(PROBE.as_uri()) + ';'
                   'console.log(JSON.stringify(await verifyGatewayImage({root:' +
                   json.dumps(str(self.image)) + '})));')
        return subprocess.run([NODE, '--input-type=module', '-e', program],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)

    def test_exact_reviewed_dockerfile_change_only(self):
        self.assertEqual(hashlib.sha256((ROOT / 'ops/dev/runtime.Dockerfile').read_bytes()).hexdigest(),
                         '21ee8641969bc2eb92a91d1dcde28ed90e6420433bb022f1a25d1237c7eec152')

    def test_private_umask_negative_0700_ancestor_models_uid10001_denial(self):
        for name in DIRECTORIES:
            info = (self.image / name).stat()
            self.assertEqual(stat.S_IMODE(info.st_mode), 0o700)
            # Root-owned0700 has no traverse bit for different UID/GID10001.
            self.assertEqual(info.st_mode & 0o001, 0)
        result = self.probe()
        self.assertNotEqual(result.returncode, 0, 'Probe must reject pre-fix0700 ancestors')
        self.assertIn(b'AssertionError', result.stderr)

    def test_packaging_preserves_all_other_bytes_owners_modes_and_private_context(self):
        before = inventory(self.image)
        host_before = inventory(self.dest)
        self.apply_packaging_step()
        after = inventory(self.image)
        self.assertEqual(set(before), set(after))
        changed = {name for name in before if before[name] != after[name]}
        self.assertEqual(changed, set(DIRECTORIES))
        for name in DIRECTORIES:
            self.assertEqual(after[name], before[name][:2] + (0o755, None))
            self.assertEqual(after[name][2] & 0o022, 0)
        self.assertEqual(inventory(self.dest), host_before)
        self.assertEqual(stat.S_IMODE(self.dest.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE(self.gateway.stat().st_mode), 0o644)
        self.assertEqual(hashlib.sha256(self.gateway.read_bytes()).hexdigest(), GATEWAY_SHA)
        result = self.probe()
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        proof = json.loads(result.stdout.decode())
        self.assertEqual(proof['scope'], 'ORDINARY_USER_FIXTURE')
        self.assertEqual(proof['dynamicImport'], 'PASS')

    def test_actual_import_fails_for_inaccessible_ancestor(self):
        self.apply_packaging_step()
        # The fixture owner cannot emulate a different UID. Mode000 is the
        # ordinary-user effective-access negative; actual root0700/UID10001
        # negative is mandatory at the human image gate.
        denied = self.image / 'ops'
        denied.chmod(0)
        try:
            result = subprocess.run([NODE, '--input-type=module', '-e',
                                     'await import(' + json.dumps(self.gateway.as_uri()) + ');'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(b'ERR_MODULE_NOT_FOUND', result.stderr)
        finally:
            denied.chmod(0o755)

    def test_probe_rejects_gateway_mutation_file_mode_and_missing_file(self):
        self.apply_packaging_step()
        original = self.gateway.read_bytes()
        self.gateway.write_bytes(original + b'\n// unexpected mutation\n')
        self.assertNotEqual(self.probe().returncode, 0)
        self.gateway.write_bytes(original)
        self.gateway.chmod(0o666)
        self.assertNotEqual(self.probe().returncode, 0)
        self.gateway.chmod(0o644)
        self.gateway.unlink()
        self.assertNotEqual(self.probe().returncode, 0)

    def test_image_cli_refuses_agent_uid_and_permission_overrides(self):
        result = subprocess.run([NODE, str(PROBE)], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=15)
        self.assertNotEqual(result.returncode, 0)
        result = subprocess.run([NODE, str(PROBE), '--fixture'], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=15)
        self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
