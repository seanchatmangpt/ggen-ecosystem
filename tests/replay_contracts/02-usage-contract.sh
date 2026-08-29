#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(encoding="utf-8")
needle = 'usage: $0 [--dry-run] [--image-repo <repo>] <receipt.json>'
if needle not in text:
    raise SystemExit(f"missing replay contract: {needle}")
PY
# semantic-fingerprint: 6c89f0f116f91b8198cf57721f21516434201dcbe73838e6da2fb6695c27bde2
