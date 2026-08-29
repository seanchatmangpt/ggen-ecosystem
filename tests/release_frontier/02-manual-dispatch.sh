#!/usr/bin/env bash
set -euo pipefail
# WS2 multi-arch release frontier contract 02
# semantic-fingerprint: manual-dispatch
# classification: present-invariant
# admitted-base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'workflow_dispatch:' .github/workflows/ggen-ecosystem-container.yml
