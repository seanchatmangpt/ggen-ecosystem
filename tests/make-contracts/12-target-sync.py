#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^sync(?:\\s*:[^\\n]*)?$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH target-sync")
    raise SystemExit(1)
print("ALIVE target-sync: sync target is present")
