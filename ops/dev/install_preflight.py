#!/usr/bin/env python3
"""Run only from a verified root-owned reviewed snapshot, never the repository."""
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import platform
import re
import stat
import subprocess
import sys

REVIEW_ROOT = Path('/var/lib/gcreation-perf-review')
SOURCE = Path('/home/codexperf/projects/gcreation-performance')
ENVIRONMENT = Path('/etc/gcreation-perf-dev/runtime.env')
NOFOLLOW = os.O_NOFOLLOW


def require_root_owned(path, regular=False, private=False):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ValueError('Unsafe root path')
    current = Path('/')
    info = current.lstat()
    for part in path.parts[1:]:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise ValueError('Root-owned non-writable path required')
    if regular and (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1):
        raise ValueError('Root-owned regular file required')
    if private and stat.S_IMODE(info.st_mode) != 0o600:
        raise ValueError('Private root file must be 0600')


def verify_archive(path, approved_sha):
    if not re.fullmatch('[0-9a-f]{64}', approved_sha):
        raise ValueError('Exact human-approved SHA-256 required')
    require_root_owned(path, regular=True, private=True)
    if path.stat().st_size > 64 * 1024 * 1024:
        raise ValueError('Archive size limit')
    if hashlib.sha256(path.read_bytes()).hexdigest() != approved_sha:
        raise ValueError('Root staging SHA-256 mismatch')


def verify_snapshot(snapshot, approved_sha, commit):
    if not re.fullmatch('[0-9a-f]{40}', commit) or snapshot != REVIEW_ROOT / commit / 'snapshot':
        raise ValueError('Only fixed root-owned reviewed snapshot permitted')
    require_root_owned(snapshot)
    archive = snapshot.parent / 'reviewed-source.tar.gz'
    verify_archive(archive, approved_sha)
    approval = snapshot.parent / 'approved.json'
    require_root_owned(approval, regular=True, private=True)
    metadata = json.loads(approval.read_text())
    if metadata['commit'] != commit or metadata['archive_sha256'] != approved_sha:
        raise ValueError('Approval identity mismatch')
    actual = {}
    for path in snapshot.rglob('*'):
        require_root_owned(path, regular=not path.is_dir())
        if path.is_file():
            actual[str(path.relative_to(snapshot))] = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != metadata['files'] or (snapshot / 'REVIEW_SOURCE_COMMIT').read_text() != commit + '\n':
        raise ValueError('Reviewed snapshot content mismatch')


def reject_stale_request(source=SOURCE):
    # Anchor the developer-owned input directories; never follow their symlinks.
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in (source / '.ops').parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = nxt
        try:
            os.stat('deploy-dev.request', dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        raise ValueError('Stale deployment request blocks watcher installation')
    finally:
        os.close(fd)


def secure_environment():
    require_root_owned(ENVIRONMENT, regular=True, private=True)
    values = {}
    allowed = {'ENGINE_SECRET', 'DENIED_IPS', 'MIN_AVAILABLE_KB', 'MAX_MEMORY_PRESSURE', 'PRICING_JSON'}
    for line in ENVIRONMENT.read_text().splitlines():
        if not line or line.startswith('#'):
            continue
        key, value = line.split('=', 1)
        if key not in allowed or key in values or not value:
            raise ValueError('Unexpected runtime environment entry')
        values[key] = value
    if not re.fullmatch('[0-9a-f]{64}', values.get('ENGINE_SECRET', '')) or not values.get('DENIED_IPS'):
        raise ValueError('Secure engine secret and denied host IPs required')
    for value in values['DENIED_IPS'].split(','):
        if not ipaddress.ip_address(value).is_global:
            raise ValueError('Denied host IP must be globally routable')
    if not 256000 <= int(values.get('MIN_AVAILABLE_KB', '1200000')) <= 20000000:
        raise ValueError('Unsafe memory threshold')
    if not 0 <= float(values.get('MAX_MEMORY_PRESSURE', '10')) <= 50:
        raise ValueError('Unsafe pressure threshold')
    if 'PRICING_JSON' in values:
        json.loads(values['PRICING_JSON'])
    return values


def output(args):
    result = subprocess.run(args, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode or len(result.stdout) > 65536:
        raise RuntimeError('Installer prerequisite failed')
    return result.stdout.decode()


def preflight(snapshot, approved_sha, commit):
    if os.geteuid() != 0:
        raise PermissionError('Human-only reviewed installation')
    verify_snapshot(snapshot, approved_sha, commit)
    reject_stale_request()
    secure_environment()
    if platform.machine() != 'x86_64':
        raise ValueError('Reviewed runtime requires linux/amd64')
    info = json.loads(output(['docker', 'info', '--format', '{{json .}}']))
    if info.get('CgroupDriver') != 'systemd' or info.get('OSType') != 'linux' or info.get('NCPU', 0) < 4:
        raise ValueError('Expected Docker/systemd resource controls unavailable')
    version = output(['systemctl', '--version']).splitlines()[0].split()
    if version[0] != 'systemd' or int(version[1]) < 239:
        raise ValueError('Required systemd capabilities unavailable')
    if not output(['systemctl', 'show', '--property=Version', '--value']).strip():
        raise ValueError('Systemd manager unavailable')
    for path in ('/usr/local/lib', '/etc/systemd/system', '/var/lib', '/etc'):
        require_root_owned(Path(path))
    for path in ('/usr/local/lib/gcreation-perf-dev', '/var/lib/gcreation-perf-dev', '/etc/gcreation-perf-dev'):
        if os.path.lexists(path):
            require_root_owned(Path(path))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise ValueError('Require SNAPSHOT APPROVED_ARCHIVE_SHA256 REVIEWED_COMMIT')
    snapshot = Path(sys.argv[1])
    if Path(__file__) != snapshot / 'ops/dev/install_preflight.py':
        raise ValueError('Preflight must execute from the reviewed root snapshot')
    preflight(snapshot, sys.argv[2], sys.argv[3])
