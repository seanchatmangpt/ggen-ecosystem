#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-amd64-consumer-crown
! grep -Fq 'amd64 consumer' .github/workflows/ggen-ecosystem-container.yml
