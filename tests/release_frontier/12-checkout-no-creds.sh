#!/usr/bin/env bash
set -euo pipefail
# fingerprint: checkout-no-creds
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'persist-credentials: false' .github/workflows/ggen-ecosystem-container.yml
