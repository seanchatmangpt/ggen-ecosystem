#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-platform-receipt-field
! grep -Fq 'platform_identity' .github/workflows/ggen-ecosystem-container.yml
