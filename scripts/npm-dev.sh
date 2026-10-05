#!/bin/sh
set -eu
cd /home/codexperf/projects/gcreation-performance
export PATH="$PWD/.ops/toolchain/node_modules/node/bin:$PATH"
export npm_config_cache="$PWD/.ops/npm-cache"
exec "$PWD/.ops/toolchain/node_modules/node/bin/node" /opt/plesk/node/26/lib/node_modules/npm/bin/npm-cli.js "$@"
