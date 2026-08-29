#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='>"$OUTPUT_FILE" 2>"$STDERR_FILE"'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: b24515a6c2801355bff7c04258d9acfc81da12863d5a8ea8805651f50ed9ff21
