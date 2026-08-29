#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'sh scripts/verify-provenance\\.sh'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH verify-shell-fallback")
    raise SystemExit(1)
print("ALIVE verify-shell-fallback: verify supports shell fallback")
