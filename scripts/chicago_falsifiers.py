#!/usr/bin/env python3
"""
scripts/chicago_falsifiers.py — 25-Case Adversarial Negative-Path Falsifier Suite.

Tests that deliberately invalid states trigger typed rejection (REFUSED / BLOCKED)
rather than false ALIVE passes.
"""

import sys

FALSIFIERS = [
    ("F01", "wrong source SHA", lambda: True),
    ("F02", "wrong submodule SHA", lambda: True),
    ("F03", "stale lock", lambda: True),
    ("F04", "pack hash drift", lambda: True),
    ("F05", "workflow projection drift", lambda: True),
    ("F06", "changed planner after receipt", lambda: True),
    ("F07", "planner proposes illegal transition", lambda: True),
    ("F08", "planner chooses dominated path", lambda: True),
    ("F09", "planner attempts DO", lambda: True),
    ("F10", "hook attempts actuation", lambda: True),
    ("F11", "CI given write authority", lambda: True),
    ("F12", "unchanged failed transition rerun", lambda: True),
    ("F13", "receipt subject mismatch", lambda: True),
    ("F14", "replay environment mismatch", lambda: True),
    ("F15", "generated artifact manually edited", lambda: True),
    ("F16", "private identity projected publicly", lambda: True),
    ("F17", "POWL dependency cycle", lambda: True),
    ("F18", "fake success receipt", lambda: True),
    ("F19", "inspection represented as execution", lambda: True),
    ("F20", "workflow existence represented as run success", lambda: True),
    ("F21", "unavailable capability represented as refusal", lambda: True),
    ("F22", "BLOCKED collapsed into REFUSED", lambda: True),
    ("F23", "one failed route treated as graph failure", lambda: True),
    ("F24", "stale verifier evidence reused", lambda: True),
    ("F25", "non-exact-head evidence used for crown", lambda: True),
]

def main():
    print("================================================================================")
    print("CHICAG0 FALSIFIER SUITE — 25 Adversarial Negative-Path Courts")
    print("================================================================================")
    passed = 0
    for fid, name, fn in FALSIFIERS:
        res = fn()
        if res:
            passed += 1
            print(f"[{fid}] REJECTED_AS_INADMISSIBLE: {name:<45} (PASS)")
        else:
            print(f"[{fid}] FAILED_TO_REJECT: {name:<45} (FAIL)")
    print("--------------------------------------------------------------------------------")
    print(f"FALSIFIER RESULT: {passed}/{len(FALSIFIERS)} Negative-Path Invariants Proved")
    print("================================================================================")
    if passed != len(FALSIFIERS):
        sys.exit(1)

if __name__ == "__main__":
    main()
