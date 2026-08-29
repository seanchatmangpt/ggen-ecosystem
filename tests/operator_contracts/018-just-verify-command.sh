#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @bash scripts/verify-provenance.sh' 'Justfile'
