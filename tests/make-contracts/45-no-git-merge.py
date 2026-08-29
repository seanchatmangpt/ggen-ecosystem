#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^(?![\\s\\S]*\\bgit merge\\b)[\\s\\S]*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH no-git-merge")
    raise SystemExit(1)
print("ALIVE no-git-merge: operator surface contains no git merge actuation")
