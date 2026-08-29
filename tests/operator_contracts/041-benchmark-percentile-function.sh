#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'def pct(p):' 'scripts/benchmark.sh'
