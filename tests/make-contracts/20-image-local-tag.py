#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\s*docker build -t ggen-ecosystem:local \\.\\s*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH image-local-tag")
    raise SystemExit(1)
print("ALIVE image-local-tag: image builds local composed tag")
