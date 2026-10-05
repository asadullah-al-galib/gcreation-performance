#!/bin/bash
# HUMAN ONLY: review then execute as root. Never run by the coding agent.
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Human root installation required' >&2; exit 1; }
SOURCE=/home/codexperf/projects/gcreation-performance
DEST=/usr/local/lib/gcreation-perf-dev
python3 "$SOURCE/ops/dev/deploy_controller.py" --check-install-source
# This installer and controller must be reviewed together before root execution.
install -d -o root -g root -m 0755 "$DEST"
for file in deploy_controller.py deploy-dev.sh runtime.Dockerfile seccomp_profile.json; do
  install -o root -g root -m 0644 "$SOURCE/ops/dev/$file" "$DEST/$file"
done
chmod 0755 "$DEST/deploy-dev.sh"
for file in gcreation-perf-dev-deploy.service gcreation-perf-dev-deploy.path gcreation-perf-dev.slice; do
  install -o root -g root -m 0644 "$SOURCE/ops/dev/$file" "/etc/systemd/system/$file"
done
install -d -o root -g root -m 0700 /var/lib/gcreation-perf-dev /etc/gcreation-perf-dev
if [[ ! -f /etc/gcreation-perf-dev/runtime.env ]]; then
  umask 077
  python3 - <<'PY' > /etc/gcreation-perf-dev/runtime.env
import secrets
print('ENGINE_SECRET=' + secrets.token_hex(32))
print('DENIED_IPS=')
PY
fi
# Trusted image definition only; repository Dockerfiles are never built by the watcher.
docker build -f "$DEST/runtime.Dockerfile" -t gcreation-perf-dev-runtime:0.1 "$DEST"
systemctl daemon-reload
systemctl enable --now gcreation-perf-dev-deploy.path
printf '%s\n' 'Installed DEV-only watcher. Review README for proxy and request procedure.'
