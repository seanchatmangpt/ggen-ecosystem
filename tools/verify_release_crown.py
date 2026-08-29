#!/usr/bin/env python3
"""Verify release-crown contracts against repository doctrine.

Zero third-party dependencies. Each JSON contract is independently executable:
  python3 tools/verify_release_crown.py --contract contracts/release-crown/01-....json
Aggregate:
  python3 tools/verify_release_crown.py contracts/release-crown
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

ALLOWED_FAILURE = {
    "UNKNOWN","PARTIAL_ALIVE","ALIVE","BLOCKED","BUILD_BROKEN","UNSUPPORTED",
}

def typed_standing_ok(value: str) -> bool:
    return value in ALLOWED_FAILURE or value.startswith("REFUSED:")

def row_standing(text: str, requirement: str) -> str | None:
    m = re.search(
        rf"^\|\s*{re.escape(requirement)}\s*\|.*?\|\s*\*\*(?:([^*]+))\*\*",
        text,
        flags=re.MULTILINE,
    )
    if not m:
        return None
    return m.group(1).split()[0].strip()

def verify_contract(root: Path, contract: dict) -> tuple[bool,str]:
    source = root / contract["source"]
    if not source.is_file():
        return False, f"missing source: {contract['source']}"
    text = source.read_text(encoding="utf-8")
    kind = contract["kind"]

    if kind == "contains":
        ok = contract["expected"] in text
    elif kind == "standing_row":
        actual = row_standing(text, contract["requirement"])
        ok = actual == contract["expected"]
        if not ok:
            return False, f"{contract['requirement']} standing={actual!r}, expected={contract['expected']!r}"
    elif kind == "ordered_tokens":
        pos = -1
        ok = True
        for token in contract["tokens"]:
            pos2 = text.find(token, pos + 1)
            if pos2 < 0:
                ok = False
                break
            pos = pos2
    elif kind == "regex_count":
        actual = len(re.findall(contract["pattern"], text, flags=re.MULTILINE))
        ok = actual == int(contract["count"])
        if not ok:
            return False, f"count={actual}, expected={contract['count']}"
    elif kind == "clause_token":
        clause = contract["clause"]
        ok = clause in text and contract["token"] in clause
    else:
        return False, f"unsupported kind: {kind}"

    return (True, "PASS") if ok else (False, contract["remediation"])

def validate_schema(contract: dict) -> tuple[bool,str]:
    required = {"id","source","kind","failure_standing","remediation"}
    missing = sorted(required - contract.keys())
    if missing:
        return False, "missing keys: " + ",".join(missing)
    if not typed_standing_ok(contract["failure_standing"]):
        return False, f"invalid typed standing: {contract['failure_standing']}"
    kinds = {"contains","standing_row","ordered_tokens","regex_count","clause_token"}
    if contract["kind"] not in kinds:
        return False, f"unsupported kind: {contract['kind']}"
    return True, "PASS"

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("contracts", nargs="?", default="contracts/release-crown")
    ap.add_argument("--root", default=".")
    ap.add_argument("--contract")
    ap.add_argument("--self-test", action="store_true")
    ns = ap.parse_args()
    root = Path(ns.root)

    paths = [Path(ns.contract)] if ns.contract else sorted(Path(ns.contracts).glob("*.json"))
    results = []
    for p in paths:
        c = json.loads(p.read_text(encoding="utf-8"))
        schema_ok, schema_detail = validate_schema(c)
        if ns.self_test:
            ok, detail = schema_ok, schema_detail
        elif schema_ok:
            ok, detail = verify_contract(root, c)
        else:
            ok, detail = False, schema_detail
        results.append({
            "contract": str(p),
            "id": c.get("id"),
            "ok": ok,
            "standing": "ALIVE" if ok else c.get("failure_standing","UNKNOWN"),
            "detail": detail,
        })

    failed = [r for r in results if not r["ok"]]
    report = {
        "schema":"https://ggen.dev/contracts/release-crown/v1",
        "checked":len(results),
        "passed":len(results)-len(failed),
        "failed":len(failed),
        "results":results,
    }
    print(json.dumps(report, sort_keys=True))
    return 0 if not failed else 1

if __name__ == "__main__":
    raise SystemExit(main())
