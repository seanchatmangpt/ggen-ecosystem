#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-not-multiarch-verified
grep -Fq 'not yet multi-arch verified' docs/DEFINITION-OF-DONE.md
