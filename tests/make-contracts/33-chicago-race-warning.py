#!/usr/bin/env python3
from pathlib import Path
import re, sys
text = Path(sys.argv[1] if len(sys.argv)>1 else "Makefile").read_text()
pattern = 'do not run `make chicago` casually mid-swarm'
if not re.search(pattern, text, re.MULTILINE):
    print("REFUSED:MAKE_CONTRACT_MISMATCH chicago-race-warning")
    raise SystemExit(1)
print("ALIVE chicago-race-warning: chicago documents build-race hazard")
