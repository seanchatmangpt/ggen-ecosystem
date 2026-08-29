#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='if [[ "$RECORDED_NORMALIZED" != sha256:* ]]; then'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 9d7379f50dc528daa46299d21f59777d27d932fff463cef1be0f3bfa74279b2e
