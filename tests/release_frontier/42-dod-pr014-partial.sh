#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-pr014-partial
grep -Fq '| PR-014 | Definition of Done executable | **PARTIAL_ALIVE** |' docs/DEFINITION-OF-DONE.md
