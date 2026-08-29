#!/usr/bin/env bash
set -euo pipefail
# fingerprint: tag-push-trigger
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq "- 'v[0-9]+.[0-9]+.[0-9]+'" .github/workflows/ggen-ecosystem-container.yml
