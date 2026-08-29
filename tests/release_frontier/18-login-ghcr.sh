#!/usr/bin/env bash
set -euo pipefail
# fingerprint: login-ghcr
grep -Fq 'registry: ghcr.io' .github/workflows/ggen-ecosystem-container.yml
