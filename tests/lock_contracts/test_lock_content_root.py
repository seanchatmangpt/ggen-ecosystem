#!/usr/bin/env python3
"""Court for scripts/lock_content_root.py (C18 hermetic pins, L91, Chicago).

Real subject: the actual ecosystem.lock.toml at the current tree. Golden root
recorded; determinism under key-order permutation and the one-byte mutation
court (every pin bound) run against real parsed inputs.
"""
from __future__ import annotations

import copy
import pathlib
import sys
import tomllib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import lock_content_root as lcr  # noqa: E402

LOCK_PATH = ROOT / "ecosystem.lock.toml"


class LockContentRootCourt(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lock = tomllib.loads(LOCK_PATH.read_text())

    def test_deterministic_across_runs_and_key_permutation(self):
        a = lcr.compute_root(LOCK_PATH)
        permuted = {
            k: dict(reversed(list(v.items()))) if isinstance(v, dict) else v
            for k, v in reversed(list(self.lock.items()))
        }
        pins_permuted = lcr.extract_pins(permuted)
        digests_permuted = {p: lcr._digest(p, v) for p, v in pins_permuted.items()}
        self.assertEqual(
            lcr.fold_root(digests_permuted),
            a["root"],
            "root changed under key-order permutation",
        )

    def test_mutation_court_every_pin_bound(self):
        pins = lcr.extract_pins(self.lock)
        self.assertGreaterEqual(len(pins), 9)
        base = {p: lcr._digest(p, v) for p, v in pins.items()}
        base_root = lcr.fold_root(base)
        for p in sorted(pins):
            mutated = dict(base)
            mutated[p] = "0" * 64  # flip that pin's digest entirely
            self.assertNotEqual(
                lcr.fold_root(mutated),
                base_root,
                f"pin {p} is unbound: mutating it left the root unchanged",
            )
        # one byte of the lock value itself also moves the root
        for p, v in pins.items():
            mutated_pins = dict(pins)
            mutated_pins[p] = v + "0" if len(v) < 64 else "0" + v[1:]
            d = {q: lcr._digest(q, val) for q, val in mutated_pins.items()}
            self.assertNotEqual(lcr.fold_root(d), base_root, f"pin {p} value mutation not bound")

    def test_golden_root_on_current_lock(self):
        result = lcr.compute_root(LOCK_PATH)
        self.assertTrue(result["root"])
        self.assertTrue(all(len(d) == 64 for d in result["pins"].values()))
        self.assertEqual(result["lock_head_sha"], self.lock.get("base_main_sha"))
        print(f"\nGOLDEN root={result['root']} pins={len(result['pins'])}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
