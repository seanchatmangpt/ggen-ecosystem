#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @python3 scripts/dod_engine.py' 'Justfile'
