#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'PARALLEL=16' 'scripts/stress_test.sh'
