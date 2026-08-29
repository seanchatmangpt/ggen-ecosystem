#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @cat ontology/gates.ttl 2>/dev/null || python3 scripts/ecosystem_alive.py --explain' 'Justfile'
