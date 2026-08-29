#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    *) echo "unknown flag: $1" >&2; exit 2 ;;' 'scripts/benchmark.sh'
