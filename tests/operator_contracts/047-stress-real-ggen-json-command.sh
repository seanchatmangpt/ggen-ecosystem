#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    ggen sync run --dry-run --format json-pretty > "$SCRATCH/run-$i.json" 2>"$SCRATCH/run-$i.stderr"' 'scripts/stress_test.sh'
