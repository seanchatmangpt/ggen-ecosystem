#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-receipt-alive
grep -Fq '| PR-019 | Receipt | **ALIVE** |' docs/DEFINITION-OF-DONE.md
