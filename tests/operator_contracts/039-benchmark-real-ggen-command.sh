#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '  ggen sync run --dry-run --format quiet >/dev/null 2>&1' 'scripts/benchmark.sh'
