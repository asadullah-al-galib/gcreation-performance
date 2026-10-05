#!/bin/sh
set -eu
cd /home/codexperf/projects/gcreation-performance
export npm_config_cache="$PWD/.ops/npm-cache"
npm install --prefix .ops/toolchain --no-save node@24.21.0
.ops/toolchain/node_modules/node/bin/node --version
