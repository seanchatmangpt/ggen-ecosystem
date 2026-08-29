#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '\\|\\| cat docs/DEFINITION-OF-DONE\\.md'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH dod-fallback-cat")
    raise SystemExit(1)
print("ALIVE dod-fallback-cat: dod falls back to whole document")
