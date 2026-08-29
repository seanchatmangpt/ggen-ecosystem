#!/usr/bin/env bash
set -euo pipefail
TARGET="${1:-tests/replay_check.sh}"
python3 - "$TARGET" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
needle='if [[ -n "$IMAGE_REPO_OVERRIDE" ]]; then'
if needle not in text: raise SystemExit(f'missing replay contract: {needle}')
PY
# semantic-fingerprint: e98c56927a428d90b79efdfea3d4fc4cfad10f68372800aeffd070c9a146f911
