#!/usr/bin/env python3
"""Validate one or more public-adoption scenario contracts with stdlib only."""
import json, pathlib, re, sys

ALLOWED = {"UNKNOWN","PARTIAL_ALIVE","ALIVE","BLOCKED","BUILD_BROKEN","UNSUPPORTED","REFUSED"}
REQUIRED = {
    "work_key": str, "title": str, "hypothesis": str, "subject": str,
    "setup": list, "action": str, "oracle": list, "expected_standing": str,
    "reason_code": str, "authority": str, "receipt_required": bool,
    "rollback": str, "next_route": str, "semantic_fingerprint": str,
}
FINGERPRINT = re.compile(r"^SJ-[0-9]{3}:[a-z0-9-]+$")

def verify(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    errors = []
    for key, typ in REQUIRED.items():
        if key not in data:
            errors.append(f"missing:{key}")
        elif not isinstance(data[key], typ):
            errors.append(f"type:{key}")
    standing = data.get("expected_standing")
    if standing not in ALLOWED:
        errors.append("standing:invalid")
    if standing != "ALIVE" and not data.get("reason_code"):
        errors.append("reason_code:required")
    if standing == "ALIVE" and data.get("reason_code") != "NONE":
        errors.append("reason_code:alive-must-be-NONE")
    if data.get("authority") != "SELECT_CONSTRUCT_ONLY":
        errors.append("authority:ambient-DO-refused")
    if data.get("receipt_required") is not True:
        errors.append("receipt:required")
    if not FINGERPRINT.fullmatch(data.get("semantic_fingerprint", "")):
        errors.append("semantic_fingerprint:invalid")
    for key in ("setup", "oracle"):
        if key in data and isinstance(data[key], list) and not data[key]:
            errors.append(f"{key}:empty")
    return errors

def main(argv):
    paths = [pathlib.Path(p) for p in argv[1:]]
    if not paths:
        paths = sorted(pathlib.Path("tests/public-adoption/scenarios").glob("*.json"))
    if not paths:
        print("UNKNOWN no scenario contracts found", file=sys.stderr)
        return 2
    failed = 0
    for path in paths:
        try:
            errors = verify(path)
        except Exception as exc:
            errors = [f"parse:{type(exc).__name__}:{exc}"]
        if errors:
            failed += 1
            print(f"REFUSED {path}: {','.join(errors)}")
        else:
            print(f"ALIVE {path}")
    print(f"checked={len(paths)} passed={len(paths)-failed} failed={failed}")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
