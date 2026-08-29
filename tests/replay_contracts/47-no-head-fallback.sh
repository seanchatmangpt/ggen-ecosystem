#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='refusing rather than pulling or substituting a newer tag/HEAD'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: ac41fb6a1210bda18e3a2e5281599f1679d8db24d72b5bf2036177b2b4b5ceb5
