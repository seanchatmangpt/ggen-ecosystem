#!/usr/bin/env bash
set -euo pipefail
# fingerprint: checkout-recursive
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'submodules: recursive' .github/workflows/ggen-ecosystem-container.yml
