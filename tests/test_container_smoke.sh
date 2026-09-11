#!/usr/bin/env bash
# Compatibility entrypoint. Historically this file mixed real container execution
# with modeled gate states, dry-runs, fabricated receipts, and synthetic ALIVE crowns.
# Those surfaces are intentionally removed from the Chicago authority path.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec bash "$SCRIPT_DIR/chicago_consumer.sh" "$@"
