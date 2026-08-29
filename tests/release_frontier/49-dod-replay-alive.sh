#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-replay-alive
grep -Fq '| PR-020 | Replay | **ALIVE** |' docs/DEFINITION-OF-DONE.md
