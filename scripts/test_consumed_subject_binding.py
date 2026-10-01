#!/usr/bin/env python3
"""Local executable court for consumed-subject verification.

Usage:
  python scripts/test_consumed_subject_binding.py EXACT_MARKETPLACE ADJACENT_MARKETPLACE DIRTY_MARKETPLACE

The caller constructs disposable fixtures. This court never mutates donor repositories.
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

VERIFIER=Path(__file__).with_name("verify_standing_imports.py")
MANIFEST=Path(__file__).parents[1]/"contracts/standing-imports/v26.9.30.json"

def verify(root: Path):
    p=subprocess.run([sys.executable,str(VERIFIER),"--manifest",str(MANIFEST),"--marketplace-root",str(root)],text=True,capture_output=True)
    return p.returncode,json.loads(p.stdout)

def court(root: Path, code: int, refusal: str | None):
    rc,r=verify(root)
    assert rc==code,(rc,r)
    assert r["authority"]=="NONE"
    assert r["imported_do_authority"]=="forbidden"
    if refusal is None:
        assert r["standing"]=="ALIVE" and not r["refusals"],r
    else:
        assert refusal in r["refusals"],r

def main():
    if len(sys.argv)!=4:
        raise SystemExit("usage: test_consumed_subject_binding.py EXACT ADJACENT DIRTY")
    court(Path(sys.argv[1]),0,None)
    court(Path(sys.argv[2]),2,"MARKETPLACE_SUBJECT_SUBSTITUTION")
    court(Path(sys.argv[3]),2,"MARKETPLACE_SUBJECT_DIRTY")
    print("consumed-subject court: ALIVE")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
