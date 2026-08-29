#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-platform-digest-evidence
! grep -Fq 'platform digest' .github/workflows/ggen-ecosystem-container.yml
