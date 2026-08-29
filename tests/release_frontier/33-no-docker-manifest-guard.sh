#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-docker-manifest-guard
! grep -Fq 'application/vnd.docker.distribution.manifest.list.v2+json' .github/workflows/ggen-ecosystem-container.yml
