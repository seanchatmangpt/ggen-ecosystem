#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys
root=Path(__file__).resolve().parents[1]
verifier=root/"scripts/verify-receipt.sh"
fixtures=sorted((root/"tests/receipt-conformance").glob("*.invalid.json"))
if not fixtures:
    print("BUILD_BROKEN no receipt conformance fixtures",file=sys.stderr); raise SystemExit(2)
bad=[]
for f in fixtures:
    p=subprocess.run([str(verifier),str(f)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
    if p.returncode != 1: bad.append((f.name,p.returncode,p.stderr))
if bad:
    for row in bad: print("FAIL",*row,file=sys.stderr)
    raise SystemExit(1)
print(f"ALIVE {len(fixtures)}/{len(fixtures)} invalid receipt fixtures correctly refused")
