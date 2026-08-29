#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='IMAGE_REF="${IMAGE_REPO}@${CONTAINER_DIGEST}"'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: edc5519a50bf456f8e3a92c1cfdeef0a6bb64bec74899f8de3002b6d67a25066
