#!/usr/bin/env bash
set -euo pipefail
# fingerprint: workflow-contents-read
# base: 16e82dfd3701231d5ebc994104043e77654d62c4
grep -Fq 'contents: read' .github/workflows/ggen-ecosystem-container.yml
