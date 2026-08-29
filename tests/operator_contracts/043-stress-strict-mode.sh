#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'set -euo pipefail' 'scripts/stress_test.sh'
