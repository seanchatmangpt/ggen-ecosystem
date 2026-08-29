#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='echo "replay_check: unknown flag: $1" >&2'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: dff6e876c50a4a174af02b88c65951c1926aa2fb96b6dcc9ee9e1756783a1ac0
