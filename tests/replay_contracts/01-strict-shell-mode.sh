#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(encoding="utf-8")
needle = 'set -euo pipefail'
if needle not in text:
    raise SystemExit(f"missing replay contract: {needle}")
PY
# semantic-fingerprint: 2cd32e207bba6f7aaa53d48f4d5e26452f79b7b8e96d43163227dda898b0d287
