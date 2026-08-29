#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-unsupported-arch-refusal
! grep -Fq 'UNSUPPORTED_ARCH' .github/workflows/ggen-ecosystem-container.yml
