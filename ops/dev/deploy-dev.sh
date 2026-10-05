#!/bin/sh
# Installed immutable by the human. No arguments or repository shell sourcing.
set -eu
[ "$#" -eq 0 ] || exit 64
exec /usr/bin/python3 /usr/local/lib/gcreation-perf-dev/deploy_controller.py
