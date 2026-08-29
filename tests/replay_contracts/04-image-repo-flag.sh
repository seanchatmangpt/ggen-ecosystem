#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='--image-repo)'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 610febb0f79b036a1e0863f6d26f33770e99afe968102bdc398dfd11668ceba2
