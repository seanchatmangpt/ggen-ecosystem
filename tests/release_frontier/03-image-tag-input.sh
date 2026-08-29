#!/usr/bin/env bash
set -euo pipefail
# WS2 multi-arch release frontier contract 03
# semantic-fingerprint: image-tag-input
# classification: present-invariant
# admitted-base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'image_tag:' .github/workflows/ggen-ecosystem-container.yml
