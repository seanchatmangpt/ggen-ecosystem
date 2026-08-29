#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\s*ggen sync run --dry-run\\n\\s*ggen sync run\\s*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH sync-direct-ggen")
    raise SystemExit(1)
print("ALIVE sync-direct-ggen: sync uses canonical ggen CLI directly after dry-run")
