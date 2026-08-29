#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-amd64-gap
grep -Fq 'amd64 GitHub-hosted runner' docs/DEFINITION-OF-DONE.md
