#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @bash scripts/benchmark.sh --runs 20' 'Justfile'
