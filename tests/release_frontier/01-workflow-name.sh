#!/usr/bin/env bash
set -euo pipefail
# WS2 multi-arch release frontier contract 01
# semantic-fingerprint: workflow-name
# classification: present-invariant
# admitted-base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'name: GGen Ecosystem Container Build & Publish' .github/workflows/ggen-ecosystem-container.yml
