#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='if [[ -z "$RECEIPT_PATH" ]]; then'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: f679ad6f7c15f22f504f80c08937d5fb88bac09a12526641ec48cab7a9aa4d4a
