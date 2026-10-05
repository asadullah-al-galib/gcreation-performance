#!/usr/bin/env python3
"""Separate HUMAN-APPROVED PHP artifact. Never called by the auto watcher."""
import fcntl
import os
from pathlib import Path
import pwd
import re
import stat
import sys

if __name__ == '__main__':
    # -I isolates Python from developer-controlled cwd/PYTHONPATH/user-site.
    # Add only this immutable reviewed directory for the sibling helper import.
    actual = Path(__file__)
    if not re.fullmatch('/var/lib/gcreation-perf-review/[0-9a-f]{40}/snapshot/ops/dev/install-reviewed-plugin.py', str(actual)):
        raise PermissionError('Reviewed root snapshot required')
    current = Path('/')
    for part in actual.parts[1:]:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
            raise PermissionError('Immutable root-owned input required')
    sys.path.insert(0, str(actual.parent))

from install_preflight import verify_snapshot, secure_environment

WP = Path('/var/www/vhosts/gcreation.agency/dev.gcreation.agency')
FILES = {'gcreation-performance.php', 'app.js', 'app.css'}
NOFOLLOW = os.O_NOFOLLOW


def open_directory(path):
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = nxt
        return fd
    except Exception:
        os.close(fd)
        raise


def remove_tree(parent, name):
    fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=parent)
    try:
        for child in os.listdir(fd):
            info = os.stat(child, dir_fd=fd, follow_symlinks=False)
            if stat.S_ISDIR(info.st_mode):
                remove_tree(fd, child)
            else:
                os.unlink(child, dir_fd=fd)
    finally:
        os.close(fd)
    os.rmdir(name, dir_fd=parent)


def install_payload(parent, payload, secret):
    if os.geteuid() == 0:
        raise PermissionError('WordPress writes must happen after dropping root')
    if set(payload) != FILES or not re.fullmatch('[0-9a-f]{64}', secret):
        raise ValueError('Only reviewed plugin files and strong secret permitted')
    name = 'gcreation-performance'
    backup = '.gcreation-performance-human-backup'
    staging = '.gcreation-performance-human-stage'
    # Exclusive fixed staging; stale/symlink staging fails instead of following.
    os.mkdir(staging, mode=0o700, dir_fd=parent)
    fd = os.open(staging, os.O_RDONLY | os.O_DIRECTORY | NOFOLLOW, dir_fd=parent)
    moved = False
    try:
        content = dict(payload)
        content['config.php'] = ("<?php\nif (!defined('ABSPATH')) { exit; }\ndefine('GCREATION_ENGINE_SECRET', '" + secret + "');\n").encode()
        for file, data in content.items():
            out = os.open(file, os.O_WRONLY | os.O_CREAT | os.O_EXCL | NOFOLLOW, 0o600, dir_fd=fd)
            with os.fdopen(out, 'wb') as stream:
                stream.write(data); stream.flush(); os.fsync(stream.fileno())
                os.fchmod(stream.fileno(), 0o600 if file == 'config.php' else 0o644)
        os.fchmod(fd, 0o755)
        try:
            os.stat(backup, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            remove_tree(parent, backup)
        try:
            info = os.stat(name, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            if not stat.S_ISDIR(info.st_mode):
                raise ValueError('Unsafe existing DEV plugin')
            os.rename(name, backup, src_dir_fd=parent, dst_dir_fd=parent); moved = True
        try:
            os.rename(staging, name, src_dir_fd=parent, dst_dir_fd=parent)
        except Exception:
            if moved:
                os.rename(backup, name, src_dir_fd=parent, dst_dir_fd=parent)
            raise
    finally:
        os.close(fd)
        try:
            os.stat(staging, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError:
            pass
        else:
            remove_tree(parent, staging)


def human_install(snapshot, approved_sha, commit, owner_name):
    if os.geteuid() != 0 or Path(__file__) != snapshot / 'ops/dev/install-reviewed-plugin.py':
        raise PermissionError('Only human-approved root snapshot execution permitted')
    verify_snapshot(snapshot, approved_sha, commit)
    environment = secure_environment()
    site = pwd.getpwnam(owner_name)
    if site.pw_uid in (0, pwd.getpwnam('codexperf').pw_uid):
        raise ValueError('Verified DEV PHP/Plesk owner required')
    wp_fd = open_directory(WP)
    parent = open_directory(WP / 'wp-content/plugins')
    try:
        owner = os.stat('wp-config.php', dir_fd=wp_fd, follow_symlinks=False)
        if not stat.S_ISREG(owner.st_mode) or owner.st_nlink != 1 or owner.st_uid != site.pw_uid:
            raise ValueError('DEV wp-config owner does not match approved PHP owner')
        source = snapshot / 'wordpress/gcreation-performance'
        if {path.name for path in source.iterdir()} != FILES:
            raise ValueError('Unexpected reviewed plugin artifact files')
        payload = {name: (source / name).read_bytes() for name in FILES}
        lock = os.open(str(snapshot.parent / 'human-plugin.lock'), os.O_CREAT | os.O_WRONLY | NOFOLLOW, 0o600)
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            child = os.fork()
            if child == 0:
                try:
                    os.setgroups([]); os.setgid(site.pw_gid); os.setuid(site.pw_uid)
                    install_payload(parent, payload, environment['ENGINE_SECRET'])
                except Exception:
                    os._exit(1)
                os._exit(0)
            _, result = os.waitpid(child, 0)
            if result != 0:
                raise RuntimeError('Human plugin artifact step failed')
        finally:
            os.close(lock)
    finally:
        os.close(wp_fd); os.close(parent)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        raise ValueError('Require SNAPSHOT APPROVED_ARCHIVE_SHA256 REVIEWED_COMMIT DEV_PHP_OWNER')
    human_install(Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4])
