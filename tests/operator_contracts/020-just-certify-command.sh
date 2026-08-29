#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @python3 scripts/certify_ecosystem.py --root .' 'Justfile'
