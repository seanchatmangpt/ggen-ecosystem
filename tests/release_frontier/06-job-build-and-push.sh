#!/usr/bin/env bash
set -euo pipefail
# fingerprint: job-build-and-push
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'build-and-push:' .github/workflows/ggen-ecosystem-container.yml
