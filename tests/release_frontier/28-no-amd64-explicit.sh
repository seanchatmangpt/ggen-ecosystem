#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-amd64-explicit
! grep -Fq 'linux/amd64' .github/workflows/ggen-ecosystem-container.yml
