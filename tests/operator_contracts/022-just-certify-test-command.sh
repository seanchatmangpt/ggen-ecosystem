#!/usr/bin/env bash
set -euo pipefail
grep -Fq -- '    @python3 -m unittest tests.test_mfact_certification -v' 'Justfile'
