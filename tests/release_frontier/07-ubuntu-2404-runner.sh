#!/usr/bin/env bash
set -euo pipefail
# fingerprint: ubuntu-2404-runner
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'runs-on: ubuntu-24.04' .github/workflows/ggen-ecosystem-container.yml
