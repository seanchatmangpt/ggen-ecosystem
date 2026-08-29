#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='echo "replay_check: unexpected extra argument: $1" >&2'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 490b500f7f608bf921ffc7ef078f2c1d2909c803e4e8b0e4181c409335e68fd9
