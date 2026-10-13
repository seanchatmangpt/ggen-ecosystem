import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ecosystem_profile_court", ROOT / "scripts" / "ecosystem_profile_court.py"
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class EcosystemProfileCourt(unittest.TestCase):
    def test_real_graph_passes(self):
        """Court runs on the real union graph: PASS, all 4 families adjudicated."""
        code, lines = MOD.adjudicate()
        self.assertEqual(code, 0, "real graph must PASS:\n" + "\n".join(lines))
        for family in MOD.EXPECTED:
            self.assertTrue(
                any(l.startswith(f"PASS {family}:") for l in lines),
                f"missing PASS line for {family}:\n" + "\n".join(lines),
            )

    def test_sabotage_twins_fail(self):
        """Deleting one edge per predicate family must FAIL the court (exit 1)."""
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            for family in MOD.EXPECTED:
                twin = MOD.sabotage_twin(family, tmp / f"sabotaged-{family}.ttl")
                code, lines = MOD.adjudicate((twin, *MOD.SOURCES[1:]))
                self.assertEqual(
                    code, 1, f"sabotaged graph ({family}) must FAIL:\n" + "\n".join(lines)
                )

    def test_determinism(self):
        """Two adjudication runs produce identical output."""
        self.assertEqual(MOD.adjudicate(), MOD.adjudicate())


if __name__ == "__main__":
    unittest.main()
