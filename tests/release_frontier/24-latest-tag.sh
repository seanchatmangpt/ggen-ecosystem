#!/usr/bin/env bash
set -euo pipefail
# fingerprint: latest-tag
grep -Fq 'ghcr.io/seanchatmangpt/ggen-ecosystem:latest' .github/workflows/ggen-ecosystem-container.yml
