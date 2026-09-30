from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "frontier_intake.py"
MANIFEST = ROOT / "admission" / "frontier-2026-09-30.json"

spec = importlib.util.spec_from_file_location("frontier_intake", SCRIPT)
assert spec is not None and spec.loader is not None
frontier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(frontier)


class FrontierIntakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_current_manifest_is_structurally_alive(self) -> None:
        result = frontier.validate(self.manifest)
        self.assertEqual(result["owner_count"], 13)
        self.assertEqual(result["donor_count"], 19)
        self.assertGreaterEqual(result["falsifier_count"], 8)

    def test_no_do_authority(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["authority"]["do_authority"] = True
        with self.assertRaisesRegex(frontier.Refusal, "FRONTIER_DO_AUTHORITY"):
            frontier.validate(mutated)

    def test_donor_cannot_become_verify_sovereign(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["frontier_donors"][0]["authority_ceiling"] = "VERIFY"
        with self.assertRaisesRegex(frontier.Refusal, "DONOR_VERIFY_SOVEREIGNTY"):
            frontier.validate(mutated)

    def test_donor_target_must_be_canonical_owner(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["frontier_donors"][0]["target_owner"] = "seanchatmangpt/not-an-owner"
        with self.assertRaisesRegex(frontier.Refusal, "FRONTIER_UNKNOWN_OWNER"):
            frontier.validate(mutated)

    def test_duplicate_owner_refuses(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["canonical_owners"].append(copy.deepcopy(mutated["canonical_owners"][0]))
        with self.assertRaisesRegex(frontier.Refusal, "DUPLICATE_CANONICAL_OWNER"):
            frontier.validate(mutated)

    def test_sha_identity_is_exact(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["frontier_donors"][0]["sha"] = "main"
        with self.assertRaisesRegex(frontier.Refusal, "FRONTIER_SHA"):
            frontier.validate(mutated)


    def test_fleet_observation_cannot_promote_standing(self) -> None:
        mutated = copy.deepcopy(self.manifest)
        mutated["fleet_observation"]["standing"] = "ALIVE"
        with self.assertRaisesRegex(frontier.Refusal, "FLEET_OBSERVATION_PROMOTION"):
            frontier.validate(mutated)

    def test_fleet_observation_is_exhaustive_scan_source(self) -> None:
        fleet = self.manifest["fleet_observation"]
        self.assertEqual(fleet["repository"], "seanchatmangpt/chatman-ecosystem")
        self.assertEqual(fleet["observation_id"], "fleet:recent:2026-09-30:7d")
        self.assertEqual(fleet["repository_count"], 101)
        self.assertEqual(fleet["authority"], "NONE")
        self.assertEqual(fleet["standing"], "OBSERVED")

    def test_payment_donors_are_present(self) -> None:
        repos = {item["repository"] for item in self.manifest["frontier_donors"]}
        expected = {
            "seanchatmangpt/semantic_bit",
            "seanchatmangpt/a2a-rs",
            "seanchatmangpt/mcpp",
            "seanchatmangpt/dteam",
            "seanchatmangpt/autotel",
            "seanchatmangpt/mfw",
            "seanchatmangpt/yawl",
            "seanchatmangpt/cre",
            "seanchatmangpt/bcinr",
            "seanchatmangpt/gitvan",
            "seanchatmangpt/ash_kudzu",
            "seanchatmangpt/wasm4pm",
            "seanchatmangpt/process-intelligence",
            "seanchatmangpt/erlmcp",
        }
        self.assertTrue(expected.issubset(repos))

    def test_owner_graph_has_irreducible_boundaries(self) -> None:
        owners = {item["repository"] for item in self.manifest["canonical_owners"]}
        for required in {
            "seanchatmangpt/graphlaw",
            "seanchatmangpt/ash_a2a",
            "seanchatmangpt/affidavit",
            "seanchatmangpt/beam4pm",
            "seanchatmangpt/xaas",
            "seanchatmangpt/ggen-marketplace",
            "seanchatmangpt/castle",
            "seanchatmangpt/engineering-standards",
            "seanchatmangpt/ash",
            "seanchatmangpt/ggen_igniter",
        }:
            self.assertIn(required, owners)


if __name__ == "__main__":
    unittest.main()
