#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\s*ggen sync run --dry-run\\s*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH sync-dry-run")
    raise SystemExit(1)
print("ALIVE sync-dry-run: sync performs dry-run")
