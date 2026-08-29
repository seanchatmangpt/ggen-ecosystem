#!/usr/bin/env bash
set -euo pipefail
# fingerprint: dod-standard-runner-gap
grep -Fq 'standard hosted runner' docs/DEFINITION-OF-DONE.md
