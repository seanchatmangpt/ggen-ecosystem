#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-multiarch-crown
! grep -Fq 'MULTIARCH_ALIVE' .github/workflows/ggen-ecosystem-container.yml
