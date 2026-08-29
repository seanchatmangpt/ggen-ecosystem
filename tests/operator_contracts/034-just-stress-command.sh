#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @bash scripts/stress_test.sh --parallel 16' 'Justfile'
