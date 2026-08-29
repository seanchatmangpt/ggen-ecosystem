#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    --json-out) JSON_OUT="$2"; shift 2 ;;' 'scripts/benchmark.sh'
