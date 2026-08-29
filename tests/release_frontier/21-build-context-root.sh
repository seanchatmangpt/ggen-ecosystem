#!/usr/bin/env bash
set -euo pipefail
# fingerprint: build-context-root
grep -Fq 'context: .' .github/workflows/ggen-ecosystem-container.yml
