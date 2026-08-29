#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^(?![\\s\\S]*git push .*--force)[\\s\\S]*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH no-force-push")
    raise SystemExit(1)
print("ALIVE no-force-push: operator surface contains no force push")
