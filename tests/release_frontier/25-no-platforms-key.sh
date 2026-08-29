#!/usr/bin/env bash
set -euo pipefail
# fingerprint: no-platforms-key
! grep -Eq '^[[:space:]]*platforms:' .github/workflows/ggen-ecosystem-container.yml
