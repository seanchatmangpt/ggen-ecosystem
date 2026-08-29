#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'doctor: scripts/doctor\\.sh not found'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH doctor-missing-diagnostic")
    raise SystemExit(1)
print("ALIVE doctor-missing-diagnostic: doctor reports missing script")
