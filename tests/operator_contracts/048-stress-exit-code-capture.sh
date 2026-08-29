#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    echo $? > "$SCRATCH/run-$i.exit"' 'scripts/stress_test.sh'
