#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'verify: TODO -- scripts/verify-provenance\\.sh not found yet'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH verify-missing-diagnostic")
    raise SystemExit(1)
print("ALIVE verify-missing-diagnostic: verify reports absent verifier")
