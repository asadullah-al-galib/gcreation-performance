# Root trust transition — review recipe only

HOLD. These commands document a proposed future procedure for human review. They are **not an instruction or authorization to install now**. The agent must not run them. The third review must independently approve the source commit, the deterministic archive SHA-256 and this bootstrap recipe before any separate human installation decision.

The privileged boundary is: committed reviewed Git bytes → deterministic archive → archive copied as data into a root-only directory → exact human-approved hash checked on the root-owned copy → regular files safely extracted into a root-owned snapshot → reviewed installer executed from that snapshot. No script/module from the codexperf repository is executed as root. The manual bootstrap below uses only system Python and its standard library, supplied as trusted human stdin; it never imports or evaluates archive/repository code. Do not generate its stdin by reading or sourcing a repository file.

The ordinary development user can export the exact commit, without privilege:

```sh
python3 /home/codexperf/projects/gcreation-performance/ops/dev/review_archive.py FULL_40_HEX_SOURCE_COMMIT /home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-FULL_40_HEX_SOURCE_COMMIT.tar.gz
```

The exporter refuses root, reads committed blobs rather than mutable working files, rejects links/secrets and fixes ordering, uid/gid/modes, timestamps, tar format and gzip metadata. The reviewer independently verifies and approves the archive hash. The approved hash must come from that review, never a value read automatically from developer-writable metadata.

The following is a **future human-only review recipe**, with placeholders deliberately unusable. Copy the archive as DATA with system tools into the fixed root staging path; do not execute the exporter or repository installer as root. A new stage must not already exist:

```sh
set -eu
COMMIT='HUMAN_APPROVED_FULL_40_HEX_COMMIT'
APPROVED_SHA='HUMAN_APPROVED_FULL_64_HEX_ARCHIVE_SHA256'
STAGE="/var/lib/gcreation-perf-review/$COMMIT"
# System-only stdin validates exact identities and protected ancestors before
# creating any staging directory. It does not load repository code.
/usr/bin/python3 -I -c '
import os, re, stat, sys
from pathlib import Path
commit, digest = sys.argv[1:]
assert re.fullmatch("[0-9a-f]{40}", commit) and re.fullmatch("[0-9a-f]{64}", digest)
assert os.geteuid() == 0
base = Path("/var/lib/gcreation-perf-review")
for path in (Path("/var"), Path("/var/lib"), base):
    if os.path.lexists(str(path)):
        info = path.lstat()
        assert stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and not info.st_mode & 0o022
assert not os.path.lexists(str(base / commit))
' "$COMMIT" "$APPROVED_SHA"
/usr/bin/install -d -o root -g root -m 0700 /var/lib/gcreation-perf-review "$STAGE"
/usr/bin/install -o root -g root -m 0600 "/home/codexperf/projects/gcreation-performance/.ops/test-artifacts/review-source-$COMMIT.tar.gz" "$STAGE/reviewed-source.tar.gz"
/usr/bin/python3 -I - "$COMMIT" "$APPROVED_SHA" <<'PY'
import gzip, hashlib, io, json, os, re, stat, sys, tarfile
from pathlib import Path, PurePosixPath
commit, approved = sys.argv[1:]
if os.geteuid() != 0 or not re.fullmatch('[0-9a-f]{40}', commit) or not re.fullmatch('[0-9a-f]{64}', approved):
    raise ValueError('Human root and exact approved identities required')
stage = Path('/var/lib/gcreation-perf-review') / commit
archive = stage / 'reviewed-source.tar.gz'
current = Path('/')
for part in archive.parts[1:]:
    current = current / part
    info = current.lstat()
    if stat.S_ISLNK(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        raise ValueError('Unsafe root staging ownership/path')
info = archive.lstat()
if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 64 * 1024 * 1024:
    raise ValueError('Private bounded root-owned archive required')
raw = archive.read_bytes()
if hashlib.sha256(raw).hexdigest() != approved:
    raise ValueError('Root staging SHA-256 mismatch')
# Bound gzip expansion before tar metadata parsing, including PAX/GNU headers.
with gzip.GzipFile(fileobj=io.BytesIO(raw)) as compressed:
    expanded = compressed.read(96 * 1024 * 1024 + 1)
if len(expanded) > 96 * 1024 * 1024:
    raise ValueError('Compressed archive expansion limit')
# Validate every entry before creating the snapshot; never use extractall.
files = {}
total = 0
with tarfile.open(fileobj=io.BytesIO(expanded), mode='r:') as data:
    for member in data:
        name = member.name
        path = PurePosixPath(name)
        if (not member.isreg() or name.startswith('/') or str(path) != name
                or '..' in path.parts or name in files or len(files) >= 30000
                or member.size < 0 or member.size > 8 * 1024 * 1024):
            raise ValueError('Unsafe archive entry')
        total += member.size
        if total > 64 * 1024 * 1024:
            raise ValueError('Archive expansion limit')
        files[name] = data.extractfile(member).read()
if files.get('REVIEW_SOURCE_COMMIT') != (commit + '\n').encode():
    raise ValueError('Reviewed commit marker mismatch')
snapshot = stage / 'snapshot'
snapshot.mkdir(mode=0o700)  # Existing snapshot fails closed.
for name, content in sorted(files.items()):
    target = snapshot / name
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    with target.open('xb') as out:
        out.write(content)
    target.chmod(0o644)
metadata = {'commit': commit, 'archive_sha256': approved,
            'files': {name: hashlib.sha256(content).hexdigest() for name, content in files.items()}}
with (stage / 'approved.json').open('x') as out:
    os.fchmod(out.fileno(), 0o600)
    out.write(json.dumps(metadata))
PY
```

Before any future installer execution, the human provisions a root-owned 0600 `/etc/gcreation-perf-dev/runtime.env` with a 64 lowercase-hex ENGINE_SECRET, a nonempty list of the server's global public DENIED_IPS and only documented settings. Do not share its contents. Existing protected directories must be root-owned, contain no symlinks and have no group/other write access. Installation preflight checks archive/snapshot hashes and ownership, secure environment, Docker daemon health/systemd cgroup driver, x86_64, systemd version/manager, fixed paths and absence of any `.ops/deploy-dev.request` (including dangling links). It repeats the checks immediately before enabling the watcher. Nothing is installed/enabled when the initial preflight fails.

Only after a **separate future human approval**, the installer command would be:

```sh
/bin/bash "/var/lib/gcreation-perf-review/$COMMIT/snapshot/ops/dev/install-root.sh" "$APPROVED_SHA" "$COMMIT"
```

All privileged installer inputs come from that reviewed snapshot. It never uses the repository as an installer source. Installed code is immutable to codexperf; the later watcher may read repository files only as untrusted bounded data for its non-root container build. No WordPress deployment authority is given to the watcher.
