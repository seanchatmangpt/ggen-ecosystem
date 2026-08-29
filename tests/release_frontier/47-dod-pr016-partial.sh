#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-pr016-partial
grep -Fq '| PR-016 | Local GitHub Actions replay (`act`) | **PARTIAL_ALIVE** |' docs/DEFINITION-OF-DONE.md
