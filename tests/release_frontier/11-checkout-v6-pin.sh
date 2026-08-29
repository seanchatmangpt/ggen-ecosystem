#!/usr/bin/env bash
set -euo pipefail
# fingerprint: checkout-v6-pin
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803' .github/workflows/ggen-ecosystem-container.yml
