#!/usr/bin/env bash
set -euo pipefail
# fingerprint: buildpush-step
grep -Fq 'name: Build and push composed image' .github/workflows/ggen-ecosystem-container.yml
