#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = '^\\s*tests/test_container_smoke\\.sh\\s*$'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH chicago-smoke")
    raise SystemExit(1)
print("ALIVE chicago-smoke: chicago runs container smoke test")
