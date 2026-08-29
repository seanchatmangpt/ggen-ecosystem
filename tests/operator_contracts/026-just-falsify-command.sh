#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @python3 scripts/chicago_falsifiers.py' 'Justfile'
