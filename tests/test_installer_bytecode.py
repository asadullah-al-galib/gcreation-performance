"""Replay the reviewed import/verification path with ordinary-user fixture DATA."""
import hashlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Execute the actual AST nodes, not a replacement snapshot verifier. Only the
# fixed review directory and root-ownership observation are fixture substitutes.
# No installer, image preparation, Docker or host administration is executed.
REPLAY = r'''
import ast
from pathlib import Path
import sys
from unittest import mock
snapshot = Path(sys.argv[2])
actual = snapshot / 'ops/dev/prepare_image.py'
tree = ast.parse(actual.read_text())
entry = tree.body[-1].body
insert = next(node for node in entry if isinstance(node, ast.Expr)
              and isinstance(node.value, ast.Call)
              and isinstance(node.value.func, ast.Attribute)
              and node.value.func.attr == 'insert')
import_node = next(node for node in entry if isinstance(node, ast.ImportFrom)
                   and node.module == 'install_preflight')
verify = next(node for node in entry if isinstance(node, ast.Expr)
              and isinstance(node.value, ast.Call)
              and isinstance(node.value.func, ast.Name)
              and node.value.func.id == 'verify_snapshot')
def execute(nodes):
    module = ast.parse('')
    module.body = nodes
    exec(compile(ast.fix_missing_locations(module), str(actual), 'exec'), globals())
execute([insert, import_node])
preflight = sys.modules['install_preflight']
with mock.patch.object(preflight, 'REVIEW_ROOT', snapshot.parent.parent), \
        mock.patch.object(preflight, 'require_root_owned'):
    execute([verify])
print('VERIFIED')
'''


class InstallerBytecodeTests(unittest.TestCase):
    def setUp(self):
        self.assertNotEqual(os.geteuid(), 0, 'Ordinary-user tests only')
        base = ROOT / '.ops/test-artifacts'
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=str(base))
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()  # Fixture disposal, never a snapshot repair strategy.

    def invocation_flags(self, mode):
        lines = (ROOT / 'ops/dev/install-root.sh').read_text().splitlines()
        commands = [shlex.split(line) for line in lines
                    if line.startswith('/usr/bin/python3 ')
                    and '"$KIT_DIR/prepare_image.py" ' + mode + ' ' in line]
        self.assertEqual(len(commands), 1)
        command = commands[0]
        self.assertEqual(command[-4:], [mode, '$ROOT_SNAPSHOT', '$APPROVED_SHA', '$REVIEWED_COMMIT'])
        return command[0], command[1:-5]

    def fixture(self):
        commit = 'a' * 40
        stage = Path(tempfile.mkdtemp(dir=str(self.root))) / commit
        snapshot = stage / 'snapshot'
        kit = snapshot / 'ops/dev'
        kit.mkdir(parents=True)
        for name in ('install_preflight.py', 'prepare_image.py'):
            (kit / name).write_bytes((ROOT / 'ops/dev' / name).read_bytes())
        (snapshot / 'REVIEW_SOURCE_COMMIT').write_text(commit + '\n')
        archive = stage / 'reviewed-source.tar.gz'
        with tarfile.open(str(archive), 'w:gz') as data:
            for path in sorted(snapshot.rglob('*')):
                if path.is_file():
                    content = path.read_bytes()
                    member = tarfile.TarInfo(str(path.relative_to(snapshot)))
                    member.size = len(content)
                    data.addfile(member, io.BytesIO(content))
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        metadata = {'commit': commit, 'archive_sha256': digest,
                    'files': self.file_map(snapshot)}
        (stage / 'approved.json').write_text(json.dumps(metadata))
        return snapshot, digest, commit, metadata['files']

    def file_map(self, snapshot):
        return {str(path.relative_to(snapshot)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in snapshot.rglob('*') if path.is_file()}

    def replay(self, flags, mode, snapshot, digest, commit):
        return subprocess.run(['/usr/bin/python3'] + flags + ['-c', REPLAY, mode,
                              str(snapshot), digest, commit], timeout=20,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              env={'PATH': '/usr/sbin:/usr/bin:/sbin:/bin'})

    def test_old_isolated_import_invalidates_approved_snapshot(self):
        snapshot, digest, commit, approved = self.fixture()
        result = self.replay(['-I'], 'prepare', snapshot, digest, commit)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b'Reviewed snapshot content mismatch', result.stderr)
        added = set(self.file_map(snapshot)) - set(approved)
        self.assertTrue(any(name.startswith('ops/dev/__pycache__/install_preflight.')
                            and name.endswith('.pyc') for name in added), added)

    def test_prepare_and_seal_invocations_disable_bytecode_at_startup(self):
        for mode in ('prepare', 'seal'):
            executable, flags = self.invocation_flags(mode)
            self.assertEqual(executable, '/usr/bin/python3')
            self.assertEqual(flags, ['-I', '-B'])
        installer = (ROOT / 'ops/dev/install-root.sh').read_text()
        self.assertNotIn('__pycache__', installer)
        self.assertNotIn('.pyc', installer)
        self.assertNotIn('dont_write_bytecode', installer)

    def test_repaired_prepare_and_seal_preserve_exact_snapshot_file_map(self):
        for mode in ('prepare', 'seal'):
            with self.subTest(mode=mode):
                _, flags = self.invocation_flags(mode)
                snapshot, digest, commit, approved = self.fixture()
                result = self.replay(flags, mode, snapshot, digest, commit)
                self.assertEqual(result.returncode, 0, result.stderr.decode())
                self.assertEqual(result.stdout, b'VERIFIED\n')
                self.assertEqual(self.file_map(snapshot), approved)
                self.assertFalse(list(snapshot.rglob('__pycache__')))

    def test_repaired_modes_still_reject_added_and_modified_source(self):
        for mode in ('prepare', 'seal'):
            for mutation in ('added', 'modified'):
                with self.subTest(mode=mode, mutation=mutation):
                    _, flags = self.invocation_flags(mode)
                    snapshot, digest, commit, _ = self.fixture()
                    target = snapshot / ('unexpected.txt' if mutation == 'added'
                                         else 'ops/dev/prepare_image.py')
                    with target.open('a') as out:
                        out.write('\n# Unapproved fixture mutation\n')
                    result = self.replay(flags, mode, snapshot, digest, commit)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(b'Reviewed snapshot content mismatch', result.stderr)
                    self.assertFalse(list(snapshot.rglob('__pycache__')))


if __name__ == '__main__':
    unittest.main()
