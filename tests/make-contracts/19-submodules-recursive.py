#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\s*git submodule update --init --recursive\\s*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH submodules-recursive")
    raise SystemExit(1)
print("ALIVE submodules-recursive: submodules initializes recursively")
