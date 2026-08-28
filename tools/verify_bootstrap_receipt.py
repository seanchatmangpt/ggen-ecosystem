#!/usr/bin/env python3
"""Validate machine-readable bootstrap receipt contracts using only Python stdlib."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

def pointer(doc, path):
    cur=doc
    for part in path.strip("/").split("/"):
        if not part:
            continue
        cur=cur[int(part)] if isinstance(cur,list) else cur[part]
    return cur

def validate(doc, contract):
    op=contract["op"]
    actual=pointer(doc, contract["path"])
    if op=="equals":
        ok=actual==contract["expected"]
    elif op=="type":
        names={"str":str,"int":int,"bool":bool,"dict":dict,"list":list}
        ok=type(actual) is names[contract["expected"]]
    elif op=="regex":
        ok=isinstance(actual,str) and re.fullmatch(contract["expected"],actual) is not None
    elif op=="same_as":
        ok=actual==pointer(doc, contract["other_path"])
    elif op=="in":
        ok=actual in contract["expected"]
    elif op=="nonempty":
        ok=bool(actual)
    else:
        raise ValueError(f"unsupported op: {op}")
    return ok,actual

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("receipt")
    ap.add_argument("contracts")
    args=ap.parse_args()
    doc=json.loads(Path(args.receipt).read_text())
    paths=sorted(Path(args.contracts).glob("*.json"))
    if not paths:
        print("REFUSED[NO_CONTRACTS]")
        return 2
    failed=[]
    for path in paths:
        c=json.loads(path.read_text())
        ok,actual=validate(doc,c)
        print(f"{'PASS' if ok else 'FAIL'} {path.name} {c['path']} {c['op']}")
        if not ok:
            failed.append((path.name,actual,c))
    if failed:
        print(f"FAILED {len(failed)}/{len(paths)}")
        return 1
    print(f"ALIVE {len(paths)}/{len(paths)} bootstrap receipt contracts")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
