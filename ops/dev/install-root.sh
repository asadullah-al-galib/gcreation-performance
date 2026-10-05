#!/bin/bash
# HUMAN REVIEW ONLY. Execute only from the verified root-owned reviewed snapshot.
set -euo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
[[ $EUID -eq 0 && $# -eq 2 ]] || exit 64
APPROVED_SHA=$1
REVIEWED_COMMIT=$2
KIT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
ROOT_SNAPSHOT=$(dirname -- "$(dirname -- "$KIT_DIR")")
[[ "$ROOT_SNAPSHOT" == "/var/lib/gcreation-perf-review/$REVIEWED_COMMIT/snapshot" ]] || exit 65
[[ "$REVIEWED_COMMIT" =~ ^[0-9a-f]{40}$ && "$APPROVED_SHA" =~ ^[0-9a-f]{64}$ ]] || exit 65
[[ "${BASH_SOURCE[0]}" == "$KIT_DIR/install-root.sh" && ! -L "${BASH_SOURCE[0]}" ]] || exit 65
# Establish ownership of every executable input ancestor before invoking Python.
for trusted_path in /var /var/lib /var/lib/gcreation-perf-review "/var/lib/gcreation-perf-review/$REVIEWED_COMMIT" "$ROOT_SNAPSHOT" "$ROOT_SNAPSHOT/ops" "$KIT_DIR" "$KIT_DIR/install_preflight.py" "$KIT_DIR/install-root.sh"; do
  [[ ! -L "$trusted_path" && $(stat -c %u -- "$trusted_path") -eq 0 ]] || exit 65
  trusted_mode=$(stat -c %a -- "$trusted_path")
  (( (8#$trusted_mode & 022) == 0 )) || exit 65
done
/usr/bin/python3 -I "$KIT_DIR/install_preflight.py" "$ROOT_SNAPSHOT" "$APPROVED_SHA" "$REVIEWED_COMMIT"
DEST=/usr/local/lib/gcreation-perf-dev
install -d -o root -g root -m 0755 "$DEST"
for reviewed_file in deploy_controller.py deploy-dev.sh runtime.Dockerfile seccomp_profile.json install_preflight.py; do
  install -o root -g root -m 0644 "$KIT_DIR/$reviewed_file" "$DEST/$reviewed_file"
done
chmod 0755 "$DEST/deploy-dev.sh"
for reviewed_unit in gcreation-perf-dev-deploy.service gcreation-perf-dev-deploy.path gcreation-perf-dev.slice; do
  install -o root -g root -m 0644 "$KIT_DIR/$reviewed_unit" "/etc/systemd/system/$reviewed_unit"
done
install -d -o root -g root -m 0700 /var/lib/gcreation-perf-dev
# Freeze only verified reviewed manifests and trusted enforcement code.
/usr/bin/python3 -I "$KIT_DIR/prepare_image.py" prepare "$ROOT_SNAPSHOT" "$APPROVED_SHA" "$REVIEWED_COMMIT"
DOCKER_BUILDKIT=1 docker build -f "$DEST/build-context/runtime.Dockerfile" -t gcreation-perf-dev-runtime:0.1 "$DEST/build-context"
/usr/bin/python3 -I "$KIT_DIR/prepare_image.py" seal "$ROOT_SNAPSHOT" "$APPROVED_SHA" "$REVIEWED_COMMIT"
# Recheck all preflight conditions, including no trigger, immediately before enable.
/usr/bin/python3 -I "$KIT_DIR/install_preflight.py" "$ROOT_SNAPSHOT" "$APPROVED_SHA" "$REVIEWED_COMMIT"
systemctl daemon-reload
systemctl enable --now gcreation-perf-dev-deploy.path
