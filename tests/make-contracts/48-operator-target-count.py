#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\.PHONY: submodules image sync doctor verify chicago dod receipt-verify replay$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH operator-target-count")
    raise SystemExit(1)
print("ALIVE operator-target-count: phony operator surface is exactly the admitted nine targets")
