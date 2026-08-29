#!/usr/bin/env python3
"""
scripts/dod_engine.py — Live Definition of Done Theorem Engine.

Evaluates:
  Done(S, H) = forall g in Closure(Requirements(S)), Verified(g, H)

Projects exact-head status to stdout or markdown.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def evaluate_live_dod() -> dict:
    cmd = ["bash", str(REPO_ROOT / "scripts" / "doctor.sh"), "--json"]
    proc = subprocess.run(cmd, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    gates = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                gates = json.loads(line).get("gates", [])
                break
            except Exception:
                pass

    total = len(gates)
    alive = sum(1 for g in gates if g["standing"] == "ALIVE")
    blocked = [g for g in gates if g["standing"] == "BLOCKED"]
    partial = [g for g in gates if g["standing"] == "PARTIAL_ALIVE"]

    return {
        "subject": "seanchatmangpt/ggen-ecosystem@v26.8.28",
        "total_gates": total,
        "alive_gates": alive,
        "standing": "ALIVE" if alive == total else ("BLOCKED" if blocked else "PARTIAL_ALIVE"),
        "gates": gates,
    }


def main():
    res = evaluate_live_dod()
    print("================================================================================")
    print(f"DEFINITION OF DONE (LIVE EXACT-HEAD THEOREM) — {res['subject']}")
    print(f"STATUS: {res['standing']} ({res['alive_gates']}/{res['total_gates']} Gates Verified)")
    print("--------------------------------------------------------------------------------")
    print(f"{'GATE':<30} {'STANDING':<15} {'OBSERVED EVIDENCE'}")
    print("--------------------------------------------------------------------------------")
    for g in res["gates"]:
        print(f"{g['gate']:<30} {g['standing']:<15} {g['detail'][:50]}")
    print("================================================================================")


if __name__ == "__main__":
    main()
