#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    "PASS": (len(crashed) == 0) and (len(unique_hashes) == 1) and (lock_before == lock_after),' 'scripts/stress_test.sh'
