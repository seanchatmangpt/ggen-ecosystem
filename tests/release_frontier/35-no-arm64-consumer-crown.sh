#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-arm64-consumer-crown
! grep -Fq 'arm64 consumer' .github/workflows/ggen-ecosystem-container.yml
