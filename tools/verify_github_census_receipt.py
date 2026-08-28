#!/usr/bin/env python3
import json, pathlib, sys

def get_path(doc, path):
    cur = doc
    for part in path.split("."):
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    return cur

def verify(receipt, contract):
    op = contract["op"]
    value = get_path(receipt, contract["path"])
    if op == "eq":
        return value == contract["expected"]
    if op == "length":
        return len(value) == contract["expected"]
    if op == "sum_fields":
        return sum(value[k] for k in contract["fields"]) == value[contract["equals_field"]]
    raise ValueError(f"unsupported op: {op}")

def main():
    if len(sys.argv) != 3:
        print("usage: verify_github_census_receipt.py RECEIPT CONTRACT_DIR", file=sys.stderr)
        return 2
    receipt = json.loads(pathlib.Path(sys.argv[1]).read_text())
    contract_dir = pathlib.Path(sys.argv[2])
    files = sorted(contract_dir.glob("*.json"))
    failed = []
    for path in files:
        contract = json.loads(path.read_text())
        try:
            ok = verify(receipt, contract)
        except Exception as exc:
            failed.append((path.name, f"ERROR {exc}"))
            continue
        if not ok:
            failed.append((path.name, "FALSE"))
    if failed:
        for name, reason in failed:
            print(f"FAIL {name}: {reason}")
        print(f"PARTIAL_ALIVE {len(files)-len(failed)}/{len(files)} census receipt contracts")
        return 1
    print(f"ALIVE {len(files)}/{len(files)} census receipt contracts")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
