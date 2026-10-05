#!/usr/bin/env python3
"""Human-reviewed fixed DEV controller. Never execute repository code on the host."""
import fcntl
import hashlib
import ipaddress
import json
import os
import pwd
import re
import shutil
import stat
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

SOURCE = Path('/home/codexperf/projects/gcreation-performance')
STATE = Path('/var/lib/gcreation-perf-dev')
TRUSTED = Path('/usr/local/lib/gcreation-perf-dev')
IMAGE = 'gcreation-perf-dev-runtime:0.1'
NETWORK = 'gcreation-perf-dev-internal'
APP = 'gcreation-perf-dev-app'
PROXY = 'gcreation-perf-dev-proxy'
BUILDER = 'gcreation-perf-dev-build'
NOFOLLOW = getattr(os, 'O_NOFOLLOW', 0)
ALLOW = ['package.json', 'package-lock.json', 'tsconfig.json', 'tsconfig.build.json', 'eslint.config.js', '.prettierignore', 'apps', 'packages', 'tests', 'wordpress', 'ops', 'docs', 'AGENTS.md', 'REQUIREMENTS.md', 'ARCHITECTURE.md', 'SECURITY.md', 'ROADMAP.md', 'PLANS.md', 'MASTER_EXEC_PLAN.md', 'README.md']


def check_path(path):
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ValueError('Unsafe path')
    current = Path('/')
    for part in path.parts[1:]:
        current = current / part
        info = os.lstat(str(current))
        if stat.S_ISLNK(info.st_mode):
            raise ValueError('Symlink rejected: ' + str(current))
    if path.resolve() != path:
        raise ValueError('Path substitution rejected')


def open_directory(path):
    # Anchor every component, so an attacker cannot swap an ancestor between
    # validation and open. All subsequent source operations use directory FDs.
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise ValueError('Unsafe directory')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
        return fd
    except Exception:
        os.close(fd)
        raise


def copy_entry(parent_fd, name, destination, budget, exclude_private=False):
    if name in ('.', '..') or '/' in name:
        raise ValueError('Unsafe entry')
    info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    if stat.S_ISDIR(info.st_mode):
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=parent_fd)
        destination.mkdir(mode=0o755)
        try:
            for child in os.listdir(fd):
                if exclude_private and (child in ('node_modules', '__pycache__', 'config.php', '.env') or child.startswith('.env.')):
                    continue
                copy_entry(fd, child, destination / child, budget, exclude_private)
        finally:
            os.close(fd)
    elif stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
        fd = os.open(name, os.O_RDONLY | NOFOLLOW | os.O_NONBLOCK, dir_fd=parent_fd)
        try:
            opened = os.fstat(fd)
            if not stat.S_ISREG(opened.st_mode) or opened.st_nlink != 1:
                raise ValueError('File substitution rejected')
            budget[0] += 1
            if budget[0] > 30000 or opened.st_size > 8 * 1024 * 1024:
                raise ValueError('Snapshot file limit')
            with os.fdopen(fd, 'rb', closefd=False) as src, destination.open('xb') as dst:
                while True:
                    chunk = src.read(65536)
                    if not chunk:
                        break
                    budget[1] += len(chunk)
                    if budget[1] > 160 * 1024 * 1024:
                        raise ValueError('Snapshot byte limit')
                    dst.write(chunk)
            # Source snapshots use predictable build permissions. Backups retain
            # ordinary permissions, including the private generated config.
            destination.chmod(0o644 if exclude_private else stat.S_IMODE(opened.st_mode) & 0o777)
        finally:
            os.close(fd)
    else:
        raise ValueError('Symlink, hardlink or special file rejected')


def command(args, timeout=600, allow_failure=False):
    result = subprocess.run(args, timeout=timeout, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    # Do not log argv/env, which can contain credentials. Keep diagnostics bounded.
    if result.returncode and not allow_failure:
        raise RuntimeError('Trusted subprocess failed with exit ' + str(result.returncode))
    return result


def container_flags(memory, cpu):
    return ['--user', '10001:10001', '--cap-drop=ALL', '--security-opt=no-new-privileges', '--security-opt=seccomp=/usr/local/lib/gcreation-perf-dev/seccomp_profile.json', '--pids-limit=192', '--cpus=' + cpu, '--memory=' + memory, '--memory-swap=' + memory, '--cgroup-parent=gcreation-perf-dev.slice', '--log-driver=local', '--log-opt=max-size=5m', '--log-opt=max-file=2', '--init']


def docker_json(args):
    result = subprocess.run(['docker'] + args, timeout=30, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if result.returncode or len(result.stdout) > 65536:
        raise RuntimeError('Docker inspection failed')
    return json.loads(result.stdout.decode()) if result.stdout.strip() else None


def ensure_internal_network():
    listed = docker_json(['network', 'ls', '--filter', 'name=^' + NETWORK + '$', '--format', '{{json .}}'])
    if listed is None:
        command(['docker', 'network', 'create', '--driver=bridge', '--internal', '--label=gcreation.role=dev-audit', NETWORK])
    existing = docker_json(['network', 'inspect', '--format', '{{json .}}', NETWORK])
    if (not isinstance(existing, dict) or existing.get('Name') != NETWORK
            or not re.fullmatch('[0-9a-f]{64}', existing.get('Id', ''))
            or existing.get('Internal') is not True or existing.get('Driver') != 'bridge'
            or existing.get('Scope') != 'local' or (existing.get('Labels') or {}).get('gcreation.role') != 'dev-audit'):
        raise ValueError('Unsafe existing Docker network')
    identity = STATE / 'network-id'
    if identity.exists():
        if identity.read_text() != existing['Id']:
            raise ValueError('Docker network identity changed')
    else:
        with identity.open('x') as output:
            output.write(existing['Id'])
        identity.chmod(0o600)


def claim_request(ops_fd):
    name = 'deploy-dev.claimed-' + os.urandom(16).hex()
    os.rename('deploy-dev.request', name, src_dir_fd=ops_fd, dst_dir_fd=ops_fd)
    try:
        fd = os.open(name, os.O_RDONLY | NOFOLLOW | os.O_NONBLOCK, dir_fd=ops_fd)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > 256 or info.st_nlink != 1 or info.st_uid != pwd.getpwnam('codexperf').pw_uid:
                raise ValueError('Invalid request file')
            request = json.loads(os.read(fd, 257).decode())
        finally:
            os.close(fd)
        if (not isinstance(request, dict) or set(request) != {'action', 'commit'}
                or request['action'] != 'deploy' or not isinstance(request['commit'], str)
                or not re.fullmatch('[0-9a-f]{40}', request['commit'])):
            raise ValueError('Invalid fixed deployment request')
        return name, request
    except Exception:
        os.unlink(name, dir_fd=ops_fd)
        raise


def prune_releases(protected):
    releases = sorted(STATE.glob('release-*'))
    excess = max(0, len(releases) - 3)
    for old in releases:
        if excess == 0:
            break
        if old not in protected:
            check_path(old)
            shutil.rmtree(str(old))
            excess -= 1


def snapshot_digest(snapshot):
    digest = hashlib.sha256()
    for path in sorted(snapshot.rglob('*')):
        if path.is_file():
            digest.update(str(path.relative_to(snapshot)).encode())
            digest.update(b'\0')
            digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def status(ops_fd, data):
    name = 'deploy-dev.status.tmp'
    try:
        os.unlink(name, dir_fd=ops_fd)
    except FileNotFoundError:
        pass
    fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | NOFOLLOW, 0o644, dir_fd=ops_fd)
    try:
        os.write(fd, (json.dumps(data) + '\n').encode())
        os.fchmod(fd, 0o644)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.rename(name, 'deploy-dev.status', src_dir_fd=ops_fd, dst_dir_fd=ops_fd)


def health():
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open('http://127.0.0.1:3101/health', timeout=10) as response:
        data = json.load(response)
        if response.status != 200 or data.get('service') != 'gcreation-performance' or data.get('environment') != 'development':
            raise RuntimeError('Internal health failed')
    with opener.open('https://dev.gcreation.agency/', timeout=15) as response:
        if response.status != 200:
            raise RuntimeError('DEV website health failed')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def start_runtime(release):
    ensure_internal_network()
    for name in (APP, PROXY):
        command(['docker', 'rm', '-f', name], allow_failure=True)
    common = ['--restart=unless-stopped', '--env-file=/etc/gcreation-perf-dev/runtime.env', '--mount=type=bind,src=' + str(release / 'output') + ',dst=/app,readonly', '--read-only', '--tmpfs=/tmp:rw,noexec,nosuid,size=128m', '--tmpfs=/home/perfdev:rw,noexec,nosuid,size=8m']
    command(['docker', 'run', '-d', '--name', PROXY, '--network', NETWORK] + container_flags('150m', '0.5') + common + [IMAGE, 'node', 'dist/packages/scanner/src/proxy-main.js'])
    command(['docker', 'network', 'connect', 'bridge', PROXY])
    command(['docker', 'run', '-d', '--name', APP, '--network', NETWORK, '-p', '127.0.0.1:3101:3101', '--env=BIND_HOST=0.0.0.0', '--env=FETCH_BRIDGE_URL=http://' + PROXY + ':3103', '--env=BROWSER_PROXY=http://' + PROXY + ':3102', '--env=DATABASE_PATH=/data/audits.sqlite', '--mount=type=bind,src=' + str(STATE / 'data') + ',dst=/data'] + container_flags('1500m', '3.5') + common + [IMAGE, 'node', 'dist/apps/audit-service/src/main.js'])
    for _ in range(30):
        try:
            health()
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError('Runtime readiness deadline exceeded')


def deploy():
    if os.geteuid() != 0:
        raise PermissionError('Human-installed root watcher required')
    for path in (SOURCE, STATE, TRUSTED):
        check_path(path)
    source_fd = open_directory(SOURCE)
    ops_fd = os.open('.ops', os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=source_fd)
    lock = os.open(str(STATE / 'deploy.lock'), os.O_WRONLY | os.O_CREAT | NOFOLLOW, 0o600)
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    request_id = 'unknown'
    previous = STATE / 'active.json'
    prior = json.loads(previous.read_text()) if previous.exists() else None
    release = None
    claimed_name = None
    runtime_changed = False
    stage = 'request-validation'
    try:
        claimed_name, request = claim_request(ops_fd)
        environment = dict(line.split('=', 1) for line in Path('/etc/gcreation-perf-dev/runtime.env').read_text().splitlines() if '=' in line)
        if not environment.get('DENIED_IPS') or len(environment.get('ENGINE_SECRET', '')) < 32:
            raise ValueError('Human-reviewed host IP deny list and engine secret required')
        if any(not ipaddress.ip_address(value).is_global for value in environment['DENIED_IPS'].split(',')):
            raise ValueError('Denied server IPs must be valid global IP addresses')
        request_id = request['commit']
        status(ops_fd, {'state': 'RUNNING', 'commit': request_id})
        stage = 'source-snapshot'
        release = STATE / ('release-' + str(time.time_ns() if hasattr(time, 'time_ns') else int(time.time()*1000000)))
        release.mkdir(mode=0o755)
        snapshot = release / 'source'; snapshot.mkdir(mode=0o755)
        budget = [0, 0]
        for item in ALLOW:
            copy_entry(source_fd, item, snapshot / item, budget, exclude_private=True)
        digest = snapshot_digest(snapshot)
        output = release / 'output'; output.mkdir(mode=0o755); os.chown(str(output), 10001, 10001)
        # Build source is read-only. Untrusted scripts execute only inside a
        # constrained non-root container, never in the root host namespace.
        ensure_internal_network()
        runtime_changed = True
        for name in (APP, PROXY):
            command(['docker', 'rm', '-f', name], allow_failure=True)
        stage = 'non-root-build'
        command(['docker', 'rm', '-f', BUILDER], allow_failure=True)
        command(['docker', 'run', '--rm', '--name', BUILDER, '--network=bridge'] + container_flags('1500m', '3.5') + ['--mount=type=bind,src=' + str(snapshot) + ',dst=/source,readonly', '--mount=type=bind,src=' + str(output) + ',dst=/app', '--tmpfs=/tmp:rw,nosuid,size=128m', IMAGE, '/bin/sh', '-ec', 'cp -R /source/. /app/; npm ci --ignore-scripts --cache=/tmp/npm-cache; npm run format:check; npm run lint:ts; npm run typecheck; npm test; npm run build'])
        data = STATE / 'data'; data.mkdir(mode=0o700, exist_ok=True); os.chown(str(data),10001,10001)
        stage = 'runtime-health'
        start_runtime(release)
        stage = 'final-health'
        health()
        previous.write_text(json.dumps({'release':str(release), 'commit':request_id, 'snapshot_sha256':digest}))
        status(ops_fd, {'state':'COMPLETED','commit':request_id,'snapshot_sha256':digest,'health':True})
    except Exception as error:
        rollback = False
        try:
            if prior and runtime_changed:
                start_runtime(Path(prior['release'])); rollback = True
            elif runtime_changed:
                for name in (APP, PROXY):
                    command(['docker','rm','-f',name],allow_failure=True)
        except Exception:
            rollback = False
        status(ops_fd, {'state':'FAILED','commit':request_id,'error':type(error).__name__,'stage':stage,'rollback':rollback})
        raise
    finally:
        try:
            if runtime_changed:
                command(['docker', 'rm', '-f', BUILDER], allow_failure=True)
            # Failed snapshots/builds also count toward retention. Preserve both
            # the current attempt and the previous runtime needed for rollback.
            prune_releases({release, Path(prior['release']) if prior else None})
        finally:
            try:
                if claimed_name:
                    os.unlink(claimed_name, dir_fd=ops_fd)
            except FileNotFoundError:
                pass
            os.close(source_fd); os.close(ops_fd); os.close(lock)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        deploy()
    else:
        raise ValueError('No arbitrary command arguments allowed')
