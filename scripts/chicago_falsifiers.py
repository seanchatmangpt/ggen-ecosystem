#!/usr/bin/env python3
"""Executable Chicago falsifier court with paired positive controls."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
FIXTURES=ROOT/"tests"/"fixtures"/"chicago"
SHA40=re.compile(r"^[0-9a-f]{40}$"); DIGEST=re.compile(r"^sha256:[0-9a-f]{64}$"); IMMUTABLE=re.compile(r"^.+@sha256:[0-9a-f]{64}$")
def admissible(op,actual,expected):
    if op=="eq": return actual==expected
    if op=="neq": return actual!=expected
    if op=="sha40": return isinstance(actual,str) and SHA40.fullmatch(actual) is not None
    if op=="digest": return isinstance(actual,str) and DIGEST.fullmatch(actual) is not None
    if op=="immutable": return isinstance(actual,str) and IMMUTABLE.fullmatch(actual) is not None
    if op=="subset": return set(actual)<=set(expected)
    if op=="disjoint": return set(actual).isdisjoint(set(expected))
    if op=="contains": return expected in actual
    if op=="not_contains": return expected not in actual
    if op=="nonempty": return bool(actual)
    if op=="zero": return actual==0
    if op=="true": return actual is True
    if op=="false": return actual is False
    if op=="age_lte": return isinstance(actual,(int,float)) and actual<=expected
    if op=="acyclic":
        graph=actual; visiting=set(); visited=set()
        def visit(node):
            if node in visiting: return False
            if node in visited: return True
            visiting.add(node)
            if not all(visit(n) for n in graph.get(node,[])): return False
            visiting.remove(node); visited.add(node); return True
        return all(visit(n) for n in graph)
    if op=="confined":
        p=Path(actual); return not p.is_absolute() and ".." not in p.parts and str(p).startswith(expected)
    if op=="unique": return len(actual)==len(set(actual))
    if op=="same_bytes": return actual[0]==actual[1]
    if op=="ordered": return actual==sorted(actual)
    if op=="enum": return actual in expected
    raise ValueError(f"unknown operation: {op}")
def evaluate(observation,refusal):
    try: ok=admissible(observation["op"],observation.get("actual"),observation.get("expected"))
    except (KeyError,TypeError,ValueError): return "REFUSED[MALFORMED_FALSIFIER]"
    return "ALIVE" if ok else refusal
def run(fixtures=FIXTURES):
    paths=sorted(fixtures.glob("*.json")); keys=set(); fps=set(); results=[]
    for path in paths:
        item=json.loads(path.read_text()); key=item["work_key"]; fp=item["semantic_fingerprint"]
        if key in keys or fp in fps:
            results.append({"case":path.name,"standing":"REFUSED[DUPLICATE_CASE_IDENTITY]"}); continue
        keys.add(key); fps.add(fp)
        rejected=evaluate(item["invalid"],item["expected_standing"]); control=evaluate(item["control"],item["expected_standing"])
        passed=rejected==item["expected_standing"] and control=="ALIVE"
        results.append({"case":path.name,"standing":"ALIVE" if passed else "BUILD_BROKEN","invalid":rejected,"control":control})
    return {"standing":"ALIVE" if len(paths)>=50 and all(r["standing"]=="ALIVE" for r in results) else "BUILD_BROKEN","count":len(paths),"results":results}
def main():
    result=run()
    for row in result["results"]: print(f"[{row['standing']}] {row['case']}: invalid={row.get('invalid')} control={row.get('control')}")
    print(f"CHICAGO: {result['standing']} ({result['count']} executable negative/control pairs)")
    return 0 if result["standing"]=="ALIVE" else 1
if __name__=="__main__": raise SystemExit(main())

