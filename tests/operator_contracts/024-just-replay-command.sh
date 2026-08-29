#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @bash tests/determinism_check.sh' 'Justfile'
