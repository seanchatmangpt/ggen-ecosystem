#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'sh scripts/doctor\\.sh'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH doctor-shell-fallback")
    raise SystemExit(1)
print("ALIVE doctor-shell-fallback: doctor supports non-executable shell fallback")
