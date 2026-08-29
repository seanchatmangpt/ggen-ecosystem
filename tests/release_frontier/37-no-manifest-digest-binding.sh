#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-manifest-digest-binding
! grep -Fq 'manifest_digest' .github/workflows/ggen-ecosystem-container.yml
