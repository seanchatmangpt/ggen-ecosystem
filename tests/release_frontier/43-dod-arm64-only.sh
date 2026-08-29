#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-arm64-only
grep -Fq 'arm64-only' docs/DEFINITION-OF-DONE.md
