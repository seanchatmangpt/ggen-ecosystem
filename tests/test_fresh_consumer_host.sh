#!/usr/bin/env bash
# Verify both admission and refusal edges of the host fresh-consumer runner.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 <ggen-executable>" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GGEN_BIN="$(realpath "$1")"

GOOD_OUTPUT="$($SCRIPT_DIR/run-fresh-consumer-host.sh "$GGEN_BIN" 26.8.28)"
grep -q '^FRESH_CONSUMER_HOST_ALIVE$' <<<"$GOOD_OUTPUT"
grep -q '^replay=unchanged$' <<<"$GOOD_OUTPUT"

set +e
BAD_OUTPUT="$($SCRIPT_DIR/run-fresh-consumer-host.sh "$GGEN_BIN" 0.0.0 2>&1)"
BAD_STATUS=$?
set -e

if [[ $BAD_STATUS -ne 4 ]]; then
  echo "FAIL: expected version mismatch exit 4, observed $BAD_STATUS" >&2
  exit 1
fi
grep -q '^REFUSED\[GGEN_VERSION_MISMATCH\]:' <<<"$BAD_OUTPUT"

echo "FRESH_CONSUMER_HOST_CONTRACT_ALIVE"
