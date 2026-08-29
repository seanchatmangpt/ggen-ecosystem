#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'SCRATCH="$REPO_ROOT/.stress-scratch"' 'scripts/stress_test.sh'
