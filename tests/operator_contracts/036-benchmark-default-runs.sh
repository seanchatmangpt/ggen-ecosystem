#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'RUNS=20' 'scripts/benchmark.sh'
