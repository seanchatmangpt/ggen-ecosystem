#!/usr/bin/env bash
set -euo pipefail
# fingerprint: push-enabled
grep -Fq 'push: true' .github/workflows/ggen-ecosystem-container.yml
