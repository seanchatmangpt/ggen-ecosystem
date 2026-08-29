#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^dod(?:\\s*:[^\\n]*)?$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH target-dod")
    raise SystemExit(1)
print("ALIVE target-dod: dod target is present")
