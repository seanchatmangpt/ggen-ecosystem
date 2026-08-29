#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @python3 scripts/ecosystem_alive.py --apply-safe' 'Justfile'
