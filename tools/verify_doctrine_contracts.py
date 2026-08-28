#!/usr/bin/env python3
import json, pathlib, sys
root=pathlib.Path(".")
contracts=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "contracts/doctrine")
failed=[]
for f in sorted(contracts.glob("*.json")):
    c=json.loads(f.read_text())
    text=(root/c["path"]).read_text()
    if c["kind"]=="contains":
        ok=c["value"] in text
    else:
        raise SystemExit(f"unsupported kind {c['kind']}")
    if not ok: failed.append((f.name,c["path"],c["value"]))
if failed:
    for x in failed: print("FAIL",*x,sep="\t")
    raise SystemExit(1)
print(f"ALIVE {len(list(contracts.glob('*.json')))} doctrine contracts")
