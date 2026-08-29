#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\.PHONY:.*\\bchicago\\b'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH phony-chicago")
    raise SystemExit(1)
print("ALIVE phony-chicago: chicago is declared phony")
