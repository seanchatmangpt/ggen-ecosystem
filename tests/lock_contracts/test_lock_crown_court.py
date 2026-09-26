#!/usr/bin/env python3
"""Adversarial court for scripts/lock_crown_court.py (Chicago style).

The real subject (exact git revision, real lock/workflow/ontology/CHANGELOG
files, real gitlinks via `git ls-tree`) must be admitted; every mutation of
that real evidence must be refused with its typed code. No test doubles: each
case copies the real inputs and changes one fact.

The subject revision is HEAD unless LOCK_COURT_REV names another commit (used
when the tree under test is a scratch archive read through GIT_DIR).
"""
from __future__ import annotations

import copy
import datetime as dt
import os
import pathlib
import statistics
import sys
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import lock_crown_court as court  # noqa: E402

REV = os.environ.get("LOCK_COURT_REV", "HEAD")

# Regression bound for the pure evaluation (benchmark receipt:
# receipts/bench-lock-crown-court-20260926.json: median 0.83 ms over 2000
# evaluations of the v26.9.25 subject on arm64/CPython 3.14). The bound is
# ~12x that median so it trips on an algorithmic regression, not runner noise.
EVALUATE_MEDIAN_BUDGET_MS = 10.0


def codes(inputs: dict) -> set[str]:
    return {code for code, _ in court.evaluate(inputs)}


class LockCrownCourt(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.real = court.load_inputs(ROOT, REV)

    def mutated(self) -> dict:
        return copy.deepcopy(self.real)

    def replace_lock(self, inputs: dict, old: str, new: str, count: int = 1) -> dict:
        self.assertIn(old, inputs["lock_text"], msg=f"fixture drift: {old!r} not in lock")
        inputs["lock_text"] = inputs["lock_text"].replace(old, new, count)
        return inputs

    # -- admission of the real subject -------------------------------------

    def test_real_subject_is_admitted(self) -> None:
        self.assertEqual(court.evaluate(self.real), [])

    def test_evaluation_is_deterministic_under_duplicate_delivery(self) -> None:
        first = court.evaluate(self.real)
        second = court.evaluate(copy.deepcopy(self.real))
        self.assertEqual(first, second)

    def test_submodule_order_is_irrelevant(self) -> None:
        inputs = self.mutated()
        inputs["gitmodules_paths"] = list(reversed(inputs["gitmodules_paths"]))
        inputs["gitlinks"] = dict(reversed(list(inputs["gitlinks"].items())))
        self.assertEqual(court.evaluate(inputs), [])

    def test_lawful_crown_bump_stays_admitted(self) -> None:
        """A crown bump moves one pin everywhere in the lock plus the gitlink only."""
        inputs = self.mutated()
        lock = court.tomllib.loads(inputs["lock_text"])
        old = lock["submodules"]["ggen_marketplace_commit"]
        new = "f" * 40
        inputs["lock_text"] = inputs["lock_text"].replace(old, new)
        inputs["gitlinks"][lock["submodules"]["ggen_marketplace_path"]] = new
        self.assertEqual(court.evaluate(inputs), [])

    # -- malformed input ---------------------------------------------------

    def test_unparseable_lock_is_refused(self) -> None:
        inputs = self.mutated()
        inputs["lock_text"] += "\n[container\n"
        self.assertEqual(codes(inputs), {"LOCK_UNPARSEABLE"})

    def test_uppercase_pin_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        pin = lock["submodules"]["beam4pm_commit"]
        inputs = self.replace_lock(self.mutated(), f'beam4pm_commit = "{pin}"', f'beam4pm_commit = "{pin.upper()}"')
        self.assertIn("PIN_SHAPE", codes(inputs))

    def test_short_pin_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        pin = lock["submodules"]["ggen_igniter_commit"]
        inputs = self.replace_lock(self.mutated(), f'ggen_igniter_commit = "{pin}"', f'ggen_igniter_commit = "{pin[:12]}"')
        self.assertIn("PIN_SHAPE", codes(inputs))

    def test_malformed_section_pin_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        pin = lock["beam4pm"]["sha"]
        inputs = self.replace_lock(self.mutated(), f'sha = "{pin}"', f'sha = "{pin.upper()}"')
        self.assertEqual(codes(inputs), {"PIN_SHAPE"})

    def test_non_commit_marketplace_default_is_refused(self) -> None:
        inputs = self.mutated()
        old = dict(court.workflow_defaults(court.workflow_on_block(inputs["workflow_text"])))["marketplace_sha"]
        for key in ("workflow_text", "ontology_text"):
            inputs[key] = inputs[key].replace(f"default: {old}", "default: latest")
        self.assertEqual(codes(inputs), {"PIN_SHAPE"})

    def test_malformed_base_main_sha_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        inputs = self.replace_lock(
            self.mutated(), f'base_main_sha = "{lock["base_main_sha"]}"', 'base_main_sha = "main"'
        )
        self.assertEqual(codes(inputs), {"PIN_SHAPE"})

    def test_malformed_updated_at_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        stamp = lock["updated_at"]
        inputs = self.replace_lock(self.mutated(), f'updated_at = "{stamp}"', 'updated_at = "2026-09-26 05:43"')
        self.assertEqual(codes(inputs), {"UPDATED_AT_SHAPE"})

    # -- wrong digest / pin drift ------------------------------------------

    def test_igniter_lock_drift_from_gitlink_is_refused(self) -> None:
        inputs = self.mutated()
        lock = court.tomllib.loads(inputs["lock_text"])
        inputs["gitlinks"][lock["submodules"]["ggen_igniter_path"]] = "0" * 40
        self.assertEqual(codes(inputs), {"GITLINK_PIN"})

    def test_beam4pm_lock_drift_from_gitlink_is_refused(self) -> None:
        inputs = self.mutated()
        lock = court.tomllib.loads(inputs["lock_text"])
        inputs["gitlinks"][lock["submodules"]["beam4pm_path"]] = "1" * 40
        self.assertEqual(codes(inputs), {"GITLINK_PIN"})

    def test_missing_gitlink_is_refused(self) -> None:
        inputs = self.mutated()
        lock = court.tomllib.loads(inputs["lock_text"])
        del inputs["gitlinks"][lock["submodules"]["wasm4pm_path"]]
        self.assertEqual(codes(inputs), {"GITLINK_PIN"})

    def test_section_pin_left_behind_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        pin = lock["beam4pm"]["sha"]
        inputs = self.replace_lock(self.mutated(), f'sha = "{pin}"', f'sha = "{"2" * 40}"')
        self.assertEqual(codes(inputs), {"SECTION_PIN"})

    def test_pragprog_marketplace_pin_left_behind_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        pin = lock["pragprog_tps"]["marketplace_sha"]
        inputs = self.replace_lock(self.mutated(), f'marketplace_sha = "{pin}"', f'marketplace_sha = "{"3" * 40}"')
        self.assertEqual(codes(inputs), {"SECTION_PIN"})

    def test_malformed_container_digest_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        digest = lock["container"]["digest"]
        inputs = self.replace_lock(self.mutated(), f'digest = "{digest}"', f'digest = "{digest.upper()}"')
        self.assertEqual(codes(inputs), {"CONTAINER_STANDING"})

    # -- submodule set: duplicate / missing / extra --------------------------

    def test_duplicate_submodule_path_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        inputs = self.replace_lock(
            self.mutated(),
            f'wasm4pm_path = "{lock["submodules"]["wasm4pm_path"]}"',
            f'wasm4pm_path = "{lock["submodules"]["beam4pm_path"]}"',
        )
        self.assertIn("SUBMODULE_DUPLICATE", codes(inputs))

    def test_submodule_missing_from_lock_is_refused(self) -> None:
        inputs = self.mutated()
        inputs["gitmodules_paths"] = inputs["gitmodules_paths"] + ["vendor/unlocked"]
        self.assertEqual(codes(inputs), {"SUBMODULE_SET"})

    def test_lock_entry_without_submodule_is_refused(self) -> None:
        inputs = self.mutated()
        inputs["gitmodules_paths"] = [p for p in inputs["gitmodules_paths"] if p != "vendor/wasm4pm"]
        self.assertEqual(codes(inputs), {"SUBMODULE_SET"})

    # -- projection / release record ---------------------------------------

    def test_hand_edited_workflow_default_is_refused(self) -> None:
        inputs = self.mutated()
        lock = court.tomllib.loads(inputs["lock_text"])
        tag = lock["container"]["tag"]
        inputs["workflow_text"] = inputs["workflow_text"].replace(f"default: {tag}", "default: v26.9.22", 1)
        self.assertEqual(codes(inputs), {"PROJECTION_PARITY", "WORKFLOW_CONTAINER_TAG"})

    def test_stale_container_tag_in_both_projection_and_source_is_refused(self) -> None:
        inputs = self.mutated()
        tag = court.tomllib.loads(inputs["lock_text"])["container"]["tag"]
        for key in ("workflow_text", "ontology_text"):
            inputs[key] = inputs[key].replace(f"default: {tag}", "default: v26.9.22")
        self.assertEqual(codes(inputs), {"WORKFLOW_CONTAINER_TAG"})

    def test_unrecorded_marketplace_default_is_refused(self) -> None:
        inputs = self.mutated()
        wf = court.workflow_defaults(court.workflow_on_block(inputs["workflow_text"]))
        old = dict(wf)["marketplace_sha"]
        for key in ("workflow_text", "ontology_text"):
            inputs[key] = inputs[key].replace(old, "4" * 40)
        self.assertEqual(codes(inputs), {"MARKETPLACE_DEFAULT_UNRECORDED"})

    def test_missing_workflow_defaults_are_refused(self) -> None:
        inputs = self.mutated()
        for key in ("workflow_text", "ontology_text"):
            inputs[key] = inputs[key].replace("ggen_container_tag:", "renamed_tag:")
        self.assertIn("WORKFLOW_DEFAULT_MISSING", codes(inputs))

    def test_release_without_changelog_section_is_refused(self) -> None:
        inputs = self.mutated()
        release = court.tomllib.loads(inputs["lock_text"])["ggen"]["release"]
        inputs["changelog_text"] = inputs["changelog_text"].replace(f"## [{release}]", "## [v0.0.0]")
        self.assertEqual(codes(inputs), {"RELEASE_UNRECORDED"})

    def test_split_release_identity_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        release = lock["ggen"]["release"]
        inputs = self.replace_lock(self.mutated(), f'release = "{release}"', 'release = "v26.9.22"')
        self.assertIn("RELEASE_IDENTITY", codes(inputs))

    # -- unauthorized standing claims --------------------------------------

    def set_container_field(self, inputs: dict, key: str, literal: str) -> dict:
        """Set `key = literal` inside [container], inserting it if absent."""
        lines = inputs["lock_text"].split("\n")
        start = lines.index("[container]")
        end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("[")), len(lines))
        for i in range(start + 1, end):
            if lines[i].startswith(f"{key} = "):
                lines[i] = f"{key} = {literal}"
                break
        else:
            lines.insert(start + 1, f"{key} = {literal}")
        inputs["lock_text"] = "\n".join(lines)
        return inputs

    def test_alive_claim_while_republish_pending_is_refused(self) -> None:
        inputs = self.set_container_field(self.mutated(), "requires_republish", "true")
        inputs = self.set_container_field(inputs, "standing", '"ALIVE"')
        self.assertEqual(codes(inputs), {"CONTAINER_STANDING"})

    def test_republish_pending_without_typed_failure_is_refused(self) -> None:
        inputs = self.set_container_field(self.mutated(), "requires_republish", "true")
        inputs = self.set_container_field(inputs, "standing", '"BLOCKED"')
        inputs = self.set_container_field(inputs, "failure", '""')
        self.assertEqual(codes(inputs), {"CONTAINER_STANDING"})

    def test_alive_with_recorded_failure_is_refused(self) -> None:
        inputs = self.set_container_field(self.mutated(), "requires_republish", "false")
        inputs = self.set_container_field(inputs, "standing", '"ALIVE"')
        inputs = self.set_container_field(inputs, "failure", '"image missing"')
        self.assertEqual(codes(inputs), {"CONTAINER_STANDING"})

    def test_standing_outside_vocabulary_is_refused(self) -> None:
        inputs = self.set_container_field(self.mutated(), "requires_republish", "false")
        inputs = self.set_container_field(inputs, "failure", '""')
        inputs = self.set_container_field(inputs, "standing", '"PROBABLY_FINE"')
        self.assertEqual(codes(inputs), {"CONTAINER_STANDING"})

    # -- stale subject / reordering of history ------------------------------

    def test_base_not_ancestor_is_refused(self) -> None:
        inputs = self.mutated()
        inputs["base_is_ancestor"] = False
        self.assertEqual(codes(inputs), {"BASE_NOT_ANCESTOR"})

    def test_base_naming_the_subject_is_refused(self) -> None:
        lock = court.tomllib.loads(self.real["lock_text"])
        inputs = self.replace_lock(
            self.mutated(), f'base_main_sha = "{lock["base_main_sha"]}"', f'base_main_sha = "{self.real["subject_sha"]}"'
        )
        self.assertEqual(codes(inputs), {"BASE_IS_SUBJECT"})

    def test_updated_at_before_base_commit_is_refused(self) -> None:
        inputs = self.mutated()
        inputs["base_commit_time"] = inputs["subject_commit_time"] + dt.timedelta(days=1)
        self.assertIn("UPDATED_AT_STALE", codes(inputs))

    def test_future_dated_lock_is_refused(self) -> None:
        inputs = self.mutated()
        inputs["subject_commit_time"] = dt.datetime(2000, 1, 1, tzinfo=dt.timezone.utc)
        self.assertEqual(codes(inputs), {"UPDATED_AT_FUTURE"})

    # -- benchmark regression bound ----------------------------------------

    def test_evaluate_stays_within_budget(self) -> None:
        samples = []
        for _ in range(300):
            start = time.perf_counter()
            court.evaluate(self.real)
            samples.append((time.perf_counter() - start) * 1000.0)
        self.assertLess(statistics.median(samples), EVALUATE_MEDIAN_BUDGET_MS, msg=f"median={statistics.median(samples):.3f}ms")


if __name__ == "__main__":
    unittest.main()
