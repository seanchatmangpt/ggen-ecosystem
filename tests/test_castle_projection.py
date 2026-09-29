from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = ROOT / "ontology" / "castle-projection.ttl"
PROFILE = ROOT / "profiles" / "castle.ttl"
REFERENCE = ROOT / "docs" / "castle" / "reference" / "capability-matrix.md"
QUERY = ROOT / "queries" / "castle-capability-projection.rq"
VIOLATIONS = ROOT / "queries" / "castle-projection-violations.rq"
UNIQUENESS = ROOT / "queries" / "castle-projection-uniqueness.rq"


def projection_blocks() -> list[str]:
    text = ONTOLOGY.read_text()
    return [
        block
        for block in text.split("\n\n")
        if block.startswith("eco:castle-projection-")
        and "a eco:CastleCapabilityProjection" in block
    ]


def quoted(block: str, predicate: str) -> str:
    match = re.search(rf"{re.escape(predicate)}\s+\"([^\"]+)\"", block)
    if not match:
        raise AssertionError(f"missing {predicate} in block:\n{block}")
    return match.group(1)


def capability(block: str) -> str:
    match = re.search(r"eco:projectedCapability\s+eco:([A-Za-z0-9_-]+)", block)
    if not match:
        raise AssertionError(f"missing projected capability in block:\n{block}")
    return match.group(1)


class CastleProjectionContracts(unittest.TestCase):
    def test_conservation_set_is_exactly_23_remaining_repositories(self) -> None:
        blocks = projection_blocks()
        self.assertEqual(23, len(blocks))

        repos = [quoted(block, "eco:projectedRepository") for block in blocks]
        self.assertEqual(23, len(set(repos)))
        self.assertNotIn("seanchatmangpt/xaas", repos)
        self.assertNotIn("seanchatmangpt/castle", repos)

    def test_every_projection_is_exact_subject_candidate_construct_only(self) -> None:
        for block in projection_blocks():
            repo = quoted(block, "eco:projectedRepository")
            sha = quoted(block, "eco:sourceSha")
            self.assertRegex(sha, r"^[0-9a-f]{40}$", repo)
            self.assertEqual("CANDIDATE", quoted(block, "eco:projectionStanding"), repo)
            self.assertEqual("CONSTRUCT", quoted(block, "eco:authorityCeiling"), repo)
            self.assertTrue(quoted(block, "eco:projectionTarget"), repo)
            self.assertTrue(quoted(block, "eco:runtimePlacement"), repo)
            self.assertTrue(quoted(block, "eco:falsifier"), repo)

    def test_projected_capabilities_are_unique_and_non_sovereign(self) -> None:
        blocks = projection_blocks()
        capabilities = [capability(block) for block in blocks]
        self.assertEqual(23, len(set(capabilities)))

        forbidden_placements = {"RUNTIME_CORE", "CONSEQUENCE_CROWN"}
        for block in blocks:
            self.assertNotIn(
                quoted(block, "eco:runtimePlacement"),
                forbidden_placements,
                quoted(block, "eco:projectedRepository"),
            )

    def test_dispositions_are_bounded(self) -> None:
        allowed = {
            "REPLACE",
            "WRAP",
            "KEEP_KNOWLEDGE_PLANE",
            "ABSORB",
            "CANDIDATE_WRAP",
            "CANDIDATE_ABSORB",
        }
        counts: dict[str, int] = {}
        for block in projection_blocks():
            disposition = quoted(block, "eco:projectionDisposition")
            self.assertIn(disposition, allowed)
            counts[disposition] = counts.get(disposition, 0) + 1

        self.assertEqual(
            {
                "REPLACE": 1,
                "WRAP": 11,
                "KEEP_KNOWLEDGE_PLANE": 3,
                "ABSORB": 1,
                "CANDIDATE_WRAP": 3,
                "CANDIDATE_ABSORB": 4,
            },
            counts,
        )

    def test_previously_unresolved_candidates_are_projected_without_promotion(self) -> None:
        expected = {
            "seanchatmangpt/mfw": ("FormalTheoryProjection", "CANDIDATE_WRAP"),
            "seanchatmangpt/ostar": ("ProofDrivenManufactureResearch", "CANDIDATE_ABSORB"),
            "seanchatmangpt/mmdio": ("SemanticDocumentProjection", "CANDIDATE_WRAP"),
            "seanchatmangpt/wasm4pm-compat": ("ProcessEvidenceCompatibility", "CANDIDATE_WRAP"),
            "seanchatmangpt/dteam": ("CapabilityKernelResearch", "CANDIDATE_ABSORB"),
            "seanchatmangpt/mcpp": ("ProofCarryingWorkRuntimeResearch", "CANDIDATE_ABSORB"),
            "seanchatmangpt/chatman-nano-stack": ("ApplicationConstitutionResearch", "CANDIDATE_ABSORB"),
        }
        observed = {
            quoted(block, "eco:projectedRepository"): (
                capability(block),
                quoted(block, "eco:projectionDisposition"),
            )
            for block in projection_blocks()
            if quoted(block, "eco:projectedRepository") in expected
        }
        self.assertEqual(expected, observed)

    def test_profile_selects_castle_without_declaring_alive(self) -> None:
        profile = PROFILE.read_text()
        ontology = ONTOLOGY.read_text()
        self.assertIn("eco:selectsProfile eco:castle", profile)
        self.assertIn("eco:profileStanding \"CANDIDATE\"", ontology)
        self.assertNotIn('eco:profileStanding "ALIVE"', ontology)

    def test_query_courts_preserve_projection_law(self) -> None:
        self.assertIn("eco:CastleCapabilityProjection", QUERY.read_text())

        violations = VIOLATIONS.read_text()
        self.assertIn("NON_CANDIDATE_STANDING", violations)
        self.assertIn("AUTHORITY_CEILING_DRIFT", violations)
        self.assertIn("CROWN_OWNERSHIP_SMUGGLED_INTO_PROJECTION", violations)

        uniqueness = UNIQUENESS.read_text()
        self.assertIn("HAVING(COUNT(?projection) != 1)", uniqueness)

    def test_diataxis_reference_covers_the_same_23_repositories(self) -> None:
        reference = REFERENCE.read_text()
        repos = [quoted(block, "eco:projectedRepository") for block in projection_blocks()]
        for repo in repos:
            self.assertEqual(
                1,
                reference.count(f"`{repo}`"),
                f"reference projection must contain {repo} exactly once",
            )


if __name__ == "__main__":
    unittest.main()
