#!/usr/bin/env bash
set -euo pipefail
# fingerprint: ghcr-login-step
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'name: Log in to GHCR' .github/workflows/ggen-ecosystem-container.yml
