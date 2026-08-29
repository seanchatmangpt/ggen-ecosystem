#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='echo "REFUSED[$1]: $2" >&2'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 52bc7dc6a71e72056ff58a84c32230736b1c4e8eead3cd5c6694e7576d9c9098
