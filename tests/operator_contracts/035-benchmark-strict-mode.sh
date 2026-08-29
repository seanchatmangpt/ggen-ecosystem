#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- 'set -euo pipefail' 'scripts/benchmark.sh'
