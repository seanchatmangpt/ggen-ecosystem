#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\s*rm -f ggen\\.lock\\s*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH sync-cleans-lock")
    raise SystemExit(1)
print("ALIVE sync-cleans-lock: sync removes stale lock before regeneration")
