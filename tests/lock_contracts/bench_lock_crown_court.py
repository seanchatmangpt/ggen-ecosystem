#!/usr/bin/env python3
"""Deterministic timing benchmark for scripts/lock_crown_court.py.

Measures the two costs the court adds to a crown/release admission:
  load_inputs  -- real file reads + `git rev-parse/ls-tree/merge-base/show`
  evaluate     -- the pure law evaluation over the loaded evidence
and emits a receipt (identity of court + subject, environment, samples
summary, regression bound). The bound for `evaluate` is enforced in CI by
tests/lock_contracts/test_lock_crown_court.py::test_evaluate_stays_within_budget.

Usage: python3 tests/lock_contracts/bench_lock_crown_court.py [--rev REV] [--receipt PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import platform
import statistics
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import lock_crown_court as court  # noqa: E402

EVALUATE_MEDIAN_BUDGET_MS = 10.0


def summarize(samples: list[float]) -> dict:
    ordered = sorted(samples)
    return {
        "n": len(ordered),
        "median_ms": round(statistics.median(ordered), 4),
        "p95_ms": round(ordered[int(0.95 * (len(ordered) - 1))], 4),
        "max_ms": round(ordered[-1], 4),
        "min_ms": round(ordered[0], 4),
    }


def timed(fn, n: int) -> list[float]:
    samples = []
    for _ in range(n):
        start = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - start) * 1000.0)
    return samples


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default=os.environ.get("LOCK_COURT_REV", "HEAD"))
    ap.add_argument("--load-n", type=int, default=30)
    ap.add_argument("--evaluate-n", type=int, default=2000)
    ap.add_argument("--receipt")
    args = ap.parse_args()

    inputs = court.load_inputs(ROOT, args.rev)
    violations = court.evaluate(inputs)
    load = summarize(timed(lambda: court.load_inputs(ROOT, args.rev), args.load_n))
    evaluate = summarize(timed(lambda: court.evaluate(inputs), args.evaluate_n))
    court_src = (ROOT / "scripts" / "lock_crown_court.py").read_bytes()
    receipt = {
        "schema": "https://ggen.dev/receipts/bench-lock-crown-court/v1",
        "subject_rev": inputs["subject_sha"],
        "court_sha256": hashlib.sha256(court_src).hexdigest(),
        "lock_sha256": hashlib.sha256(inputs["lock_text"].encode()).hexdigest(),
        "authority": "NONE",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "court_standing": "ALIVE" if not violations else "REFUSED",
        "load_inputs": load,
        "evaluate": evaluate,
        "regression_bound": {
            "metric": "evaluate.median_ms",
            "budget_ms": EVALUATE_MEDIAN_BUDGET_MS,
            "enforced_by": "tests/lock_contracts/test_lock_crown_court.py::test_evaluate_stays_within_budget",
            "within_budget": evaluate["median_ms"] < EVALUATE_MEDIAN_BUDGET_MS,
        },
    }
    text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        pathlib.Path(args.receipt).write_text(text)
    print(text, end="")
    return 0 if receipt["regression_bound"]["within_budget"] and not violations else 1


if __name__ == "__main__":
    sys.exit(main())
