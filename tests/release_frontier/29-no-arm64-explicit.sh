#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-arm64-explicit
! grep -Fq 'linux/arm64' .github/workflows/ggen-ecosystem-container.yml
