#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='This script never runs `docker build`'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 8f339337e85cb0c73f09bcc4c577484aa5099e0202f126f2539cc4ee0455673b
