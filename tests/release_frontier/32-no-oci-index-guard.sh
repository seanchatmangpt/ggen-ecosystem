#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-oci-index-guard
! grep -Fq 'application/vnd.oci.image.index.v1+json' .github/workflows/ggen-ecosystem-container.yml
