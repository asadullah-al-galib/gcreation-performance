#!/usr/bin/env python3
"""Human-reviewed fixed DEV controller. Never execute repository code on the host."""
import fcntl
import hashlib
import gzip
import io
import tarfile
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
from pathlib import Path, PurePosixPath

SOURCE = Path('/home/codexperf/projects/gcreation-performance')
STATE = Path('/var/lib/gcreation-perf-dev')
TRUSTED = Path('/usr/local/lib/gcreation-perf-dev')
IMAGE = 'gcreation-perf-dev-runtime:0.1'
NETWORK = 'gcreation-perf-dev-internal'
EGRESS = 'gcreation-perf-dev-egress'
GATEWAY = 'gcreation-perf-dev-gateway'
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


def runtime_image():
    image = (TRUSTED / 'runtime-image-id').read_text().strip()
    if not re.fullmatch('sha256:[0-9a-f]{64}', image):
        raise ValueError('Reviewed immutable image identity required')
    return image


def ensure_network(name, internal, role, identity_name, allowed):
    listed = docker_json(['network', 'ls', '--filter', 'name=^' + name + '$', '--format', '{{json .}}'])
    if listed is None:
        flags = ['--internal'] if internal else []
        command(['docker', 'network', 'create', '--driver=bridge'] + flags + ['--label=gcreation.role=' + role, name])
    existing = docker_json(['network', 'inspect', '--format', '{{json .}}', name])
    if (not isinstance(existing, dict) or existing.get('Name') != name
            or not re.fullmatch('[0-9a-f]{64}', existing.get('Id', ''))
            or existing.get('Internal') is not internal or existing.get('Driver') != 'bridge'
            or existing.get('Scope') != 'local' or existing.get('Labels') != {'gcreation.role': role}
            or not isinstance(existing.get('Containers', {}), dict)):
        raise ValueError('Unsafe existing Docker network')
    identity = STATE / identity_name
    if identity.exists():
        if identity.read_text() != existing['Id']:
            raise ValueError('Docker network identity changed')
    else:
        with identity.open('x') as output:
            output.write(existing['Id'])
        identity.chmod(0o600)
    for identifier, attachment in existing.get('Containers', {}).items():
        attached_name = attachment.get('Name')
        if attached_name not in allowed or not re.fullmatch('[0-9a-f]{64}', identifier):
            raise ValueError('Unexpected network member')
        container = docker_json(['container', 'inspect', '--format', '{{json .}}', identifier])
        expected_role = {APP: 'app', PROXY: 'proxy', GATEWAY: 'gateway'}[attached_name]
        if (container.get('Id') != identifier or container.get('Name') != '/' + attached_name
                or container.get('Image') != runtime_image()
                or (container.get('Config', {}).get('Labels') or {}).get('gcreation.role') != expected_role):
            raise ValueError('Untrusted network member identity')
        networks = container.get('NetworkSettings', {}).get('Networks', {})
        expected_networks = {NETWORK, EGRESS} if attached_name == PROXY else {NETWORK}
        # During initial proxy startup it has only the internal interface.
        if attached_name == PROXY and set(networks) == {NETWORK} and name == NETWORK:
            expected_networks = {NETWORK}
        if set(networks) != expected_networks or networks[name].get('NetworkID') != existing['Id']:
            raise ValueError('Unexpected container network attachment')


def ensure_internal_network():
    ensure_network(NETWORK, True, 'dev-audit', 'network-id', {APP, PROXY, GATEWAY})


def ensure_egress_network():
    ensure_network(EGRESS, False, 'dev-audit-egress', 'egress-network-id', {PROXY})


def verify_dependencies(snapshot):
    baseline = json.loads((TRUSTED / 'dependency-baseline.json').read_text())
    if set(baseline) != {'package.json', 'package-lock.json'}:
        raise ValueError('Invalid reviewed dependency baseline')
    for name, expected in baseline.items():
        if not re.fullmatch('[0-9a-f]{64}', expected) or hashlib.sha256((snapshot / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Dependency manifest differs from reviewed baseline')


def artifact_snapshot(ops_fd, request, snapshot):
    # Archive is untrusted DATA. Capture one bounded byte sequence from an
    # anchored descriptor, verify it, validate all entries, then create files.
    directory = os.open('source-artifacts', os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=ops_fd)
    try:
        fd = os.open(request['commit'] + '.tar.gz', os.O_RDONLY | NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        try:
            info = os.fstat(fd)
            if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                    or info.st_uid != pwd.getpwnam('codexperf').pw_uid or info.st_size > 64 * 1024 * 1024):
                raise ValueError('Invalid source artifact')
            with os.fdopen(fd, 'rb', closefd=False) as stream:
                raw = stream.read(64 * 1024 * 1024 + 1)
        finally:
            os.close(fd)
    finally:
        os.close(directory)
    if len(raw) > 64 * 1024 * 1024 or hashlib.sha256(raw).hexdigest() != request['archive_sha256']:
        raise ValueError('Source archive SHA-256 mismatch')
    with gzip.GzipFile(fileobj=io.BytesIO(raw)) as compressed:
        expanded = compressed.read(96 * 1024 * 1024 + 1)
    if len(expanded) > 96 * 1024 * 1024:
        raise ValueError('Source archive expansion limit')
    files = {}; total = 0
    with tarfile.open(fileobj=io.BytesIO(expanded), mode='r:') as archive:
        for member in archive:
            name = member.name; path = PurePosixPath(name)
            if (not member.isreg() or name.startswith('/') or str(path) != name or '..' in path.parts
                    or name == '.' or name in files or len(files) >= 30000 or member.size < 0 or member.size > 8 * 1024 * 1024
                    or any(part in ('.git', 'node_modules', 'config.php', '.env') or part.startswith('.env.') for part in path.parts)):
                raise ValueError('Unsafe source archive entry')
            total += member.size
            if total > 64 * 1024 * 1024:
                raise ValueError('Source archive byte limit')
            files[name] = archive.extractfile(member).read()
    if files.get('REVIEW_SOURCE_COMMIT') != (request['commit'] + '\n').encode():
        raise ValueError('Source artifact commit marker mismatch')
    for name, content in sorted(files.items()):
        target = snapshot / name
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
        with target.open('xb') as output:
            output.write(content)
        target.chmod(0o644)
    verify_dependencies(snapshot)
    return snapshot_digest(snapshot)



def claim_request(ops_fd):
    name = 'deploy-dev.claimed-' + os.urandom(16).hex()
    os.rename('deploy-dev.request', name, src_dir_fd=ops_fd, dst_dir_fd=ops_fd)
    try:
        fd = os.open(name, os.O_RDONLY | NOFOLLOW | os.O_NONBLOCK, dir_fd=ops_fd)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > 512 or info.st_nlink != 1 or info.st_uid != pwd.getpwnam('codexperf').pw_uid:
                raise ValueError('Invalid request file')
            request = json.loads(os.read(fd, 513).decode())
        finally:
            os.close(fd)
        if (not isinstance(request, dict) or set(request) != {'action', 'commit', 'archive_sha256'}
                or request['action'] != 'deploy' or not isinstance(request['commit'], str)
                or not re.fullmatch('[0-9a-f]{40}', request['commit'])
                or not isinstance(request['archive_sha256'], str)
                or not re.fullmatch('[0-9a-f]{64}', request['archive_sha256'])):
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
    ensure_egress_network()
    for name in (APP, PROXY, GATEWAY):
        command(['docker', 'rm', '-f', name], allow_failure=True)
    image = runtime_image()
    common = ['--restart=unless-stopped', '--read-only', '--tmpfs=/tmp:rw,noexec,nosuid,size=128m', '--tmpfs=/home/perfdev:rw,noexec,nosuid,size=8m']
    # Trusted containers have NO source/output/data mounts, and use baked code.
    command(['docker', 'run', '-d', '--name', PROXY, '--network', NETWORK, '--label=gcreation.role=proxy', '--env-file=' + str(STATE / 'proxy.env')] + container_flags('150m', '0.5') + common + [image, 'node', '/opt/gcreation-trusted/dist/packages/scanner/src/proxy-main.js'])
    command(['docker', 'network', 'connect', EGRESS, PROXY])
    command(['docker', 'run', '-d', '--name', APP, '--network', NETWORK, '--label=gcreation.role=app', '--env-file=' + str(STATE / 'app.env'), '--env=BIND_HOST=0.0.0.0', '--env=FETCH_BRIDGE_URL=http://' + PROXY + ':3103', '--env=BROWSER_PROXY=http://' + PROXY + ':3102', '--env=DATABASE_PATH=/data/audits.sqlite', '--mount=type=bind,src=' + str(STATE / 'data') + ',dst=/data', '--mount=type=bind,src=' + str(release / 'output') + ',dst=/app,readonly'] + container_flags('1400m', '3.4') + common + [image, 'node', 'dist/apps/audit-service/src/main.js'])
    command(['docker', 'run', '-d', '--name', GATEWAY, '--network', NETWORK, '--label=gcreation.role=gateway', '--env-file=' + str(STATE / 'gateway.env'), '-p', '127.0.0.1:3101:3101'] + container_flags('100m', '0.1') + common + [image, 'node', '/opt/gcreation-trusted/ops/dev/trusted/gateway.mjs'])
    ensure_internal_network()
    ensure_egress_network()
    for _ in range(30):
        try:
            health()
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError('Runtime readiness deadline exceeded')


def build_command(snapshot, output):
    return ['docker', 'run', '--rm', '--name', BUILDER, '--network=none'] + container_flags('1500m', '3.5') + ['--read-only', '--mount=type=bind,src=' + str(snapshot) + ',dst=/source,readonly', '--mount=type=bind,src=' + str(output) + ',dst=/app', '--tmpfs=/tmp:rw,nosuid,size=128m', runtime_image(), '/bin/sh', '-ec', 'cp -R /source/. /app/; ln -s /opt/gcreation-deps/node_modules /app/node_modules; npm run format:check; npm run lint:ts; npm run typecheck; npm test; npm run build']



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
        # Root-installed helper verifies secret separation and DEV DNS deny configuration.
        from install_preflight import secure_environment, write_runtime_environments
        environment = secure_environment()
        write_runtime_environments(environment, STATE)
        request_id = request['commit']
        status(ops_fd, {'state': 'RUNNING', 'commit': request_id, 'archive_sha256': request['archive_sha256']})
        stage = 'source-snapshot'
        release = STATE / ('release-' + str(time.time_ns() if hasattr(time, 'time_ns') else int(time.time()*1000000)))
        release.mkdir(mode=0o755)
        snapshot = release / 'source'; snapshot.mkdir(mode=0o755)
        digest = artifact_snapshot(ops_fd, request, snapshot)
        output = release / 'output'; output.mkdir(mode=0o755); os.chown(str(output), 10001, 10001)
        # Build source is read-only. Untrusted scripts execute only inside a
        # constrained non-root container, never in the root host namespace.
        ensure_internal_network()
        ensure_egress_network()
        runtime_changed = True
        for name in (APP, PROXY, GATEWAY):
            command(['docker', 'rm', '-f', name], allow_failure=True)
        stage = 'non-root-build'
        command(['docker', 'rm', '-f', BUILDER], allow_failure=True)
        command(build_command(snapshot, output))
        data = STATE / 'data'; data.mkdir(mode=0o700, exist_ok=True); os.chown(str(data),10001,10001)
        stage = 'runtime-health'
        start_runtime(release)
        stage = 'final-health'
        health()
        previous.write_text(json.dumps({'release':str(release), 'commit':request_id, 'archive_sha256':request['archive_sha256'], 'snapshot_sha256':digest}))
        status(ops_fd, {'state':'COMPLETED','commit':request_id,'archive_sha256':request['archive_sha256'], 'snapshot_sha256':digest,'health':True})
    except Exception as error:
        rollback = False
        try:
            if prior and runtime_changed:
                start_runtime(Path(prior['release'])); rollback = True
            elif runtime_changed:
                for name in (APP, PROXY, GATEWAY):
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
    # Python -I excludes cwd/PYTHONPATH. Only add the validated installed directory.
    actual = Path(__file__)
    if actual != TRUSTED / 'deploy_controller.py':
        raise PermissionError('Immutable human-installed controller required')
    current = Path('/')
    for part in actual.parts[1:]:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise PermissionError('Immutable root-owned controller required')
    sys.path.insert(0, str(TRUSTED))
    if len(sys.argv) == 1:
        deploy()
    else:
        raise ValueError('No arbitrary command arguments allowed')
