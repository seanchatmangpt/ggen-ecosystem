#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-release-not-alive
grep -Fq '**The release is not `ALIVE` today.**' docs/DEFINITION-OF-DONE.md
