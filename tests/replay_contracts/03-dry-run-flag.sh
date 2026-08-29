#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text = Path(sys.argv[1]).read_text(encoding="utf-8")
needle = '--dry-run)'
if needle not in text:
    raise SystemExit(f"missing replay contract: {needle}")
PY
# semantic-fingerprint: c28876836fe47a07f38d4069517058089f9efa676ee4dfdc811d69946924699d
