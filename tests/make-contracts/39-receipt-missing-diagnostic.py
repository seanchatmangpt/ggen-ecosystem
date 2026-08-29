#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'receipt-verify: TODO -- scripts/verify-receipt\\.sh not found yet'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH receipt-missing-diagnostic")
    raise SystemExit(1)
print("ALIVE receipt-missing-diagnostic: receipt target reports absent verifier")
