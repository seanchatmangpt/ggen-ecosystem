import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
SPEC = importlib.util.spec_from_file_location("knowledge_source_court", ROOT / "scripts" / "knowledge_source_court.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class KnowledgeSourceCourt(unittest.TestCase):
    def test_real_graph_adjudicates(self):
        """Court runs on the real graph: PASS or DEGRADED, 7/7 edges adjudicated."""
        code, lines = MOD.adjudicate(MOD.GRAPH)
        self.assertIn(code, (0, 1), f"unexpected exit: {code}\n" + "\n".join(lines))
        self.assertEqual(code, 0, "real graph must not FAIL:\n" + "\n".join(lines))
        edge_line = next(l for l in lines if l.startswith("edges:"))
        self.assertIn("7 knowledgeSource objects", edge_line)
        self.assertTrue(any(l.startswith("PASS ") for l in lines), "\n".join(lines))

    def test_sabotage_twin_fails(self):
        """Deleting one knowledgeSource edge must FAIL the court (exit 1)."""
        import tempfile

        with tempfile.TemporaryDirectory() as td:
            twin = MOD.sabotage_twin(Path(td) / "sabotaged.ttl")
            code, lines = MOD.adjudicate(twin)
        self.assertEqual(code, 1, "sabotaged graph must FAIL:\n" + "\n".join(lines))

    def test_determinism(self):
        """Two adjudication runs produce identical output."""
        a = MOD.adjudicate(MOD.GRAPH)
        b = MOD.adjudicate(MOD.GRAPH)
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
