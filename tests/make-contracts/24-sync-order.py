#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'sync:\\n\\s*rm -f ggen\\.lock\\n\\s*ggen sync run --dry-run\\n\\s*ggen sync run'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH sync-order")
    raise SystemExit(1)
print("ALIVE sync-order: sync orders clean→dry-run→live")
