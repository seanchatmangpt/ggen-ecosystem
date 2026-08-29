#!/usr/bin/env bash
set -euo pipefail
# reserve fingerprint: receipt-standing-partial
# This reserve replaces the refused actor-expression guard and fences the receipt's honest release-frontier standing.
grep -Fq '`standing: PARTIAL_ALIVE` inside the receipt itself, honestly, pending the open arm64-only gap.' docs/DEFINITION-OF-DONE.md
