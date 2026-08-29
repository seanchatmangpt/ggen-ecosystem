#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'docker build -t ggen-ecosystem:local \\.$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH image-context-root")
    raise SystemExit(1)
print("ALIVE image-context-root: image context is repository root")
