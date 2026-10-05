"""Unprivileged boundary tests. No install, Docker or live filesystem mutations."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('controller', str(ROOT / 'ops/dev/deploy_controller.py'))
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


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
        controller.copy_entry(self.fd, 'module', self.root / 'copied', [0, 0])
        self.assertEqual([file.name for file in (self.root / 'copied').iterdir()], ['code.ts'])

    def test_privileged_runtime_contract(self):
        self.assertEqual(str(controller.PLUGIN), '/var/www/vhosts/gcreation.agency/dev.gcreation.agency/wp-content/plugins/gcreation-performance')
        flags = controller.container_flags('1500m', '3.5')
        for flag in ['--cap-drop=ALL','--security-opt=no-new-privileges','--pids-limit=192','--cgroup-parent=gcreation-perf-dev.slice']:
            self.assertIn(flag, flags)
        source = (ROOT / 'ops/dev/deploy_controller.py').read_text()
        self.assertNotIn('shell=True', source)
        self.assertNotIn('docker.sock', source)
        self.assertIn("'127.0.0.1:3101:3101'", source)
        self.assertIn("'--internal'", source)


if __name__ == '__main__':
    unittest.main()
