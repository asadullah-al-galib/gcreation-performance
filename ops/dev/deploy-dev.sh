#!/bin/sh
# Installed immutable by the human. No arguments or repository shell sourcing.
set -eu
[ "$#" -eq 0 ] || exit 64
exec /usr/bin/env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /usr/bin/python3 -I /usr/local/lib/gcreation-perf-dev/deploy_controller.py
