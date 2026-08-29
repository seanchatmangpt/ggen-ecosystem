#!/usr/bin/env bash
set -euo pipefail
# fingerprint: buildpush-step
# Updated 2026-08-29 -- see 06-job-build-and-push.sh for why.
grep -Fq 'name: Build and push linux/amd64' .github/workflows/ggen-ecosystem-container.yml
grep -Fq 'name: Build and push linux/arm64' .github/workflows/ggen-ecosystem-container.yml
