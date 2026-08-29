#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    "benchmark": "ggen_sync_run_dry_run_wall_clock_ms",' 'scripts/benchmark.sh'
