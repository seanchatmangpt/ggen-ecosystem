#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-partial-manifest-refusal
! grep -Fq 'PARTIAL_MANIFEST' .github/workflows/ggen-ecosystem-container.yml
