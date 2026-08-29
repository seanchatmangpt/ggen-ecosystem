#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='LOCK_FILE="$REPO_ROOT/ecosystem.lock.toml"'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: 106abf4c85b5d1d6245cc682d778d09ef2b4e9e4f136e4a638968a7687c45628
