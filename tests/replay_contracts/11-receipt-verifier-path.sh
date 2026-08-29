#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='VERIFY_SCRIPT="$REPO_ROOT/scripts/verify-receipt.sh"'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 30e7f902dec0bb57f18a656c55a654847ff0da19cfbf6bdd1913915e783d5946
