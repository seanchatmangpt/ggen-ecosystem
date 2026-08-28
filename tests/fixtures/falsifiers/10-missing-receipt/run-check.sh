#!/usr/bin/env bash
# Adapts doctor.sh check-10's exact find(1) query, pointed at this fixture's empty receipts/
# directory (no *v26.8.28*container*.json present).
set -u
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$D/fixture-root"
if [ ! -d receipts ]; then
  echo "UNKNOWN: receipts/ directory not found"; exit 1
fi
found="$(find receipts -type f -iname '*v26.8.28*' -iname '*container*.json' 2>/dev/null)"
if [ -n "$found" ]; then
  echo "ALIVE: unexpected -- receipt found in empty fixture"
  exit 1
else
  echo "REFUSED[RECEIPT_MISSING]:v26.8.28 container receipt not found under receipts/"
  exit 2
fi
