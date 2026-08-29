#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '  start=$(python3 -c '"'"'import time; print(time.time_ns())'"'"')' 'scripts/benchmark.sh'
