#!/usr/bin/env python3
"""Unprivileged, deterministic Git DATA export. Refuse root execution."""
import gzip
import hashlib
import io
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile

ROOT = Path('/home/codexperf/projects/gcreation-performance')


def export_archive(commit, destination):
    if os.geteuid() == 0:
        raise PermissionError('Archive export must run unprivileged')
    if not re.fullmatch('[0-9a-f]{40}', commit):
        raise ValueError('Full reviewed Git commit required')
    wrapper = str(ROOT / 'scripts/repo-git.sh')
    if subprocess.check_output([wrapper, 'cat-file', '-t', commit]).strip() != b'commit':
        raise ValueError('Reviewed source must be a Git commit')
    entries = subprocess.check_output([wrapper, 'ls-tree', '-rz', commit]).split(b'\0')
    files = {'REVIEW_SOURCE_COMMIT': (commit + '\n').encode()}
    total = 0
    for entry in entries:
        if not entry:
            continue
        metadata, raw_name = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        name = raw_name.decode('utf-8')
        parts = PurePosixPath(name).parts
        if (mode not in ('100644', '100755') or kind != 'blob' or name.startswith('/')
                or '..' in parts or any(p in ('.env', 'config.php') or p.startswith('.env.') for p in parts)):
            raise ValueError('Unsafe Git archive entry')
        content = subprocess.check_output([wrapper, 'cat-file', 'blob', blob])
        total += len(content)
        if len(content) > 8 * 1024 * 1024 or total > 64 * 1024 * 1024 or len(files) > 30000:
            raise ValueError('Review archive limits exceeded')
        files[name] = content
    with Path(destination).open('xb') as output:
        with gzip.GzipFile(fileobj=output, filename='', mode='wb', mtime=0, compresslevel=9) as compressed:
            with tarfile.open(fileobj=compressed, mode='w', format=tarfile.USTAR_FORMAT) as archive:
                for name, content in sorted(files.items()):
                    info = tarfile.TarInfo(name)
                    info.size = len(content); info.mode = 0o644
                    info.uid = info.gid = info.mtime = 0
                    info.uname = info.gname = 'root'
                    archive.addfile(info, io.BytesIO(content))
    return hashlib.sha256(Path(destination).read_bytes()).hexdigest()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise ValueError('Usage: unprivileged review_archive.py FULL_COMMIT NEW_ARCHIVE')
    target = Path(sys.argv[2]).absolute()
    if ROOT not in target.parents:
        raise ValueError('Archive output must remain inside project')
    if target.parent.resolve() != target.parent:
        raise ValueError('Archive output parent must not contain symlinks')
    print(export_archive(sys.argv[1], target))
