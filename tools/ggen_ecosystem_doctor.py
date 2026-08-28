#!/usr/bin/env python3
import json, sys, tomllib
from pathlib import Path

def get_dotted(obj, key):
    cur=obj
    for part in key.split("."):
        cur=cur[part]
    return cur

def scalar(s):
    if s=="true": return True
    if s=="false": return False
    try: return int(s)
    except ValueError: return s

def check(root, c):
    p=root/c["path"]
    if not p.exists(): return False, f"missing:{c['path']}"
    text=p.read_text()
    if c["predicate"]=="contains":
        ok=c["expected"] in text
    elif c["predicate"]=="toml_eq":
        key,val=c["expected"].split("=",1)
        ok=get_dotted(tomllib.loads(text),key)==scalar(val)
    else:
        return False, "unsupported-predicate"
    return ok, "pass" if ok else c["remediation"]

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else ".")
    contracts=Path(sys.argv[2] if len(sys.argv)>2 else "contracts/doctor")
    rows=[]
    for p in sorted(contracts.glob("*.json")):
        c=json.loads(p.read_text())
        ok,detail=check(root,c)
        rows.append({"id":c["id"],"ok":ok,"standing":"ALIVE" if ok else c["failure_standing"],"detail":detail})
    failed=[r for r in rows if not r["ok"]]
    report={"schema":"https://ggen.dev/doctor/v1","checked":len(rows),"passed":len(rows)-len(failed),"failed":len(failed),"results":rows}
    print(json.dumps(report,sort_keys=True))
    return 0 if not failed else 1
if __name__=="__main__":
    raise SystemExit(main())
