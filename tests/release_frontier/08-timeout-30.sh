#!/usr/bin/env bash
set -euo pipefail
# fingerprint: timeout-30
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'timeout-minutes: 30' .github/workflows/ggen-ecosystem-container.yml
