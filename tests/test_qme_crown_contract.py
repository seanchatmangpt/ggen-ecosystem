from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "qme_crown.py"
MANIFEST = ROOT / "certification" / "qme-1-crown.json"
PROFILE = ROOT / ".qme" / "profile.json"

spec = importlib.util.spec_from_file_location("qme_crown", SCRIPT)
assert spec is not None and spec.loader is not None
qme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qme)

SHA40 = re.compile(r"^[0-9a-f]{40}$")


class QmeCrownContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.profile = json.loads(PROFILE.read_text(encoding="utf-8"))

    def test_crown_is_verify_only_and_claim_has_no_authority(self) -> None:
        self.assertEqual(self.manifest["authority_ceiling"], "VERIFY")
        self.assertEqual(self.manifest["claim_authority"], "NONE")
        self.assertEqual(self.profile["authority_granted_by_projection"], "none")
        self.assertFalse(self.profile["normative"])
        self.assertFalse(self.profile["weakens_core"])

    def test_canonical_qme_subject_is_single_and_exact(self) -> None:
        canonical = self.manifest["canonical_spec"]
        expected = (
            "seanchatmangpt/chatman-ecosystem@"
            "32c47032a9cefd0ab4f0980efc32fa84505031b2"
        )
        self.assertEqual(
            f"{canonical['repository']}@{canonical['sha']}",
            expected,
        )
        self.assertEqual(self.profile["canonical_spec_subject"], expected)

    def test_participant_set_is_exact_unique_and_role_complete(self) -> None:
        participants = self.manifest["participants"]
        repos = [item["repository"] for item in participants]
        self.assertEqual(len(repos), len(set(repos)))
        expected = {
            "seanchatmangpt/graphlaw",
            "seanchatmangpt/ash_graphlaw",
            "seanchatmangpt/ash_r2rml",
            "seanchatmangpt/ash_a2a",
            "seanchatmangpt/affidavit",
            "seanchatmangpt/xaas",
            "seanchatmangpt/ggen-marketplace",
        }
        self.assertEqual(set(repos), expected)
        for item in participants:
            self.assertRegex(item["sha"], SHA40)
            self.assertTrue(item["role"])

    def test_numerical_claim_is_not_promoted_by_composition(self) -> None:
        claim = self.manifest["claim"]
        self.assertEqual(claim["target_person_years"], 500_000_000)
        self.assertEqual(
            claim["expected_claim_standing"],
            "UNSUPPORTED:INSUFFICIENT_INDEPENDENT_HUMAN_BASELINE_EVIDENCE",
        )
        self.assertEqual(claim["marketplace_candidate_sha"], "888e2374f1df9ac089ab34b82ee0ca6168caf102")

    def test_graphlaw_is_reused_as_qualification_engine(self) -> None:
        engine = self.manifest["qualification_engine"]
        self.assertEqual(engine["repository"], "seanchatmangpt/graphlaw")
        self.assertRegex(engine["sha"], SHA40)
        self.assertEqual(engine["module_path"], "src/qualification.rs")
        self.assertEqual(engine["profile_path"], "qualification/profiles/universal.json")

    def test_required_inheritance_matches_canonical_projection_contract(self) -> None:
        self.assertTrue(qme.REQUIRED_INHERITANCE.issubset(set(self.profile["inheritance"])))


if __name__ == "__main__":
    unittest.main()
