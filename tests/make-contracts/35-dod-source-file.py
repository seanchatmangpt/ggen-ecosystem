#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'docs/DEFINITION-OF-DONE\\.md'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH dod-source-file")
    raise SystemExit(1)
print("ALIVE dod-source-file: dod is grounded in Definition of Done")
