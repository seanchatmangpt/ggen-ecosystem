#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @tests/test_container_smoke.sh' 'Justfile'
