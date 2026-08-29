#!/usr/bin/env bash
set -euo pipefail
# fingerprint: version-tag
grep -Fq 'ghcr.io/seanchatmangpt/ggen-ecosystem:${{ inputs.image_tag || github.ref_name }}' .github/workflows/ggen-ecosystem-container.yml
