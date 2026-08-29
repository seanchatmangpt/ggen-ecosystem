#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-manifest-inspect-step
! grep -Fq 'imagetools inspect' .github/workflows/ggen-ecosystem-container.yml
