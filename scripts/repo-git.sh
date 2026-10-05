#!/bin/sh
set -eu
cd /home/codexperf/projects/gcreation-performance
export GIT_SSH_COMMAND='ssh -F /home/codexperf/.ssh/config'
exec git --git-dir=.ops/git-metadata --work-tree=. "$@"
