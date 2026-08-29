#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-pr009-alive
grep -Fq '| PR-009 | Immutable production consumption (GHCR digest) | **ALIVE** |' docs/DEFINITION-OF-DONE.md
