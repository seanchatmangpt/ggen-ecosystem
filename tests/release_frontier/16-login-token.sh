#!/usr/bin/env bash
set -euo pipefail
# fingerprint: login-token
grep -Fq 'password: ${{ secrets.GITHUB_TOKEN }}' .github/workflows/ggen-ecosystem-container.yml
