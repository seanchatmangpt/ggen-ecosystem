#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'LOCK_HASH_BEFORE=$(shasum -a 256 ggen.lock | awk '"'"'{print $1}'"'"')' 'scripts/stress_test.sh'
