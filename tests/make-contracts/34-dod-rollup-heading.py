#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '\\^## Roll-up'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH dod-rollup-heading")
    raise SystemExit(1)
print("ALIVE dod-rollup-heading: dod extracts roll-up heading")
