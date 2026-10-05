#!/usr/bin/env python3
"""Human-installed image preparation. Reviewed snapshot bytes only; no workspace."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

FILES = ['package.json', 'package-lock.json', 'tsconfig.json',
         'ops/dev/trusted/tsconfig.json', 'ops/dev/trusted/gateway.mjs',
         'packages/scanner/src/proxy.ts', 'packages/scanner/src/proxy-main.ts',
         'packages/shared/src/security.ts', 'packages/shared/src/auth.ts']
DEST = Path('/usr/local/lib/gcreation-perf-dev')


def prepare(snapshot):
    context = DEST / 'build-context'
    context.mkdir(mode=0o755)  # Reinstallation requires separate reviewed cleanup.
    (context / 'runtime.Dockerfile').write_bytes((snapshot / 'ops/dev/runtime.Dockerfile').read_bytes())
    baseline = {}
    for name in FILES:
        content = (snapshot / name).read_bytes()
        target = context / 'trusted-source' / name
        target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
        target.write_bytes(content); target.chmod(0o644)
        if name in ('package.json', 'package-lock.json'):
            (context / name).write_bytes(content)
            baseline[name] = hashlib.sha256(content).hexdigest()
    (DEST / 'dependency-baseline.json').write_text(json.dumps(baseline, sort_keys=True))
    (DEST / 'dependency-baseline.json').chmod(0o644)


def seal():
    result = subprocess.run(['docker', 'image', 'inspect', '--format', '{{.Id}}', 'gcreation-perf-dev-runtime:0.1'], timeout=30, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    identity = result.stdout.decode().strip()
    if result.returncode or not re.fullmatch('sha256:[0-9a-f]{64}', identity):
        raise ValueError('Reviewed image identity required')
    (DEST / 'runtime-image-id').write_text(identity + '\n')
    (DEST / 'runtime-image-id').chmod(0o644)


if __name__ == '__main__':
    if len(sys.argv) != 5 or sys.argv[1] not in ('prepare', 'seal') or os.geteuid() != 0:
        raise PermissionError('Human reviewed image installation only')
    snapshot = Path(sys.argv[2]); actual = Path(__file__)
    if actual != snapshot / 'ops/dev/prepare_image.py' or not re.fullmatch('/var/lib/gcreation-perf-review/[0-9a-f]{40}/snapshot', str(snapshot)):
        raise PermissionError('Reviewed root snapshot required')
    current = Path('/')
    for part in actual.parts[1:]:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise PermissionError('Immutable root-owned image inputs required')
    sys.path.insert(0, str(actual.parent))
    from install_preflight import verify_snapshot, require_root_owned
    verify_snapshot(snapshot, sys.argv[3], sys.argv[4])
    require_root_owned(DEST)
    if sys.argv[1] == 'prepare':
        prepare(snapshot)
    else:
        seal()
