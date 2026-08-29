#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-buildx-setup
! grep -Fq 'docker/setup-buildx-action@' .github/workflows/ggen-ecosystem-container.yml
