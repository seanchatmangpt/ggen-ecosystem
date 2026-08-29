#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @bash scripts/doctor.sh --json' 'Justfile'
