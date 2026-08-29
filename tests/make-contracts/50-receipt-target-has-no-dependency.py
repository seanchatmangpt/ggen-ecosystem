#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^receipt-verify:$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH receipt-target-has-no-dependency")
    raise SystemExit(1)
print("ALIVE receipt-target-has-no-dependency: receipt verifier has no hidden prerequisite target")
