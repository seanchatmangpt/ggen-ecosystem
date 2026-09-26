from __future__ import annotations
import importlib.util, json, shutil, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD_PATH = ROOT / "scripts" / "fleet-semantic-closure.py"
spec = importlib.util.spec_from_file_location("fleet_semantic_closure", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(mod)

class FleetSemanticClosureTests(unittest.TestCase):
    def fixture(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        for rel in ["fleet.semantic.toml", "ecosystem.lock.toml", "ontology/fleet-semantic-closure.ttl"]:
            dst = root / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dst)
        return td, root

    def test_real_repository_closes_and_replays(self):
        a = mod.qualify(ROOT)
        b = mod.qualify(ROOT)
        self.assertEqual(a, b)
        self.assertEqual("ALIVE", a["standing"])
        self.assertEqual("NONE", a["authority"])
        self.assertEqual(a["closure_digest"], a["replay_digest"])
        self.assertGreaterEqual(len(a["suppliers"]), 6)
        self.assertGreaterEqual(len(a["consumers"]), 4)

    def test_exact_subject_drift_refuses(self):
        td, root = self.fixture()
        try:
            p = root / "ecosystem.lock.toml"
            p.write_text(p.read_text().replace(
                'commit_sha = "be43abd8aa6284cc15a4dc7dc1021c59169e7f67"',
                'commit_sha = "mutable-main"'))
            with self.assertRaisesRegex(mod.Refusal, "EXACT_SUBJECT"):
                mod.qualify(root)
        finally: td.cleanup()

    def test_duplicate_capability_owner_refuses(self):
        td, root = self.fixture()
        try:
            p = root / "fleet.semantic.toml"
            p.write_text(p.read_text().replace(
                'capabilities = ["wasm-process-evidence"]',
                'capabilities = ["wasm-process-evidence", "semantic-manufacture"]'))
            with self.assertRaisesRegex(mod.Refusal, "DUPLICATE_CANONICAL_OWNER"):
                mod.qualify(root)
        finally: td.cleanup()

    def test_unowned_consumer_requirement_refuses(self):
        td, root = self.fixture()
        try:
            p = root / "fleet.semantic.toml"
            p.write_text(p.read_text().replace(
                'requires = ["interchangeable-parts", "capability-ecology"]',
                'requires = ["interchangeable-parts", "capability-ecology", "phantom"]'))
            with self.assertRaisesRegex(mod.Refusal, "UNOWNED_CAPABILITY"):
                mod.qualify(root)
        finally: td.cleanup()

    def test_unconsumed_capability_refuses(self):
        td, root = self.fixture()
        try:
            p = root / "fleet.semantic.toml"
            p.write_text(p.read_text().replace(
                'capabilities = ["wasm-process-evidence"]',
                'capabilities = ["wasm-process-evidence", "orphan"]'))
            with self.assertRaisesRegex(mod.Refusal, "UNCONSUMED_CAPABILITY"):
                mod.qualify(root)
        finally: td.cleanup()

    def test_authority_widening_refuses(self):
        td, root = self.fixture()
        try:
            p = root / "fleet.semantic.toml"
            p.write_text(p.read_text().replace('authority_ceiling = "NONE"', 'authority_ceiling = "DO"'))
            with self.assertRaisesRegex(mod.Refusal, "AUTHORITY_WIDENING"):
                mod.qualify(root)
        finally: td.cleanup()

    def test_ontology_semantic_loss_refuses(self):
        td, root = self.fixture()
        try:
            p = root / "ontology/fleet-semantic-closure.ttl"
            p.write_text(p.read_text().replace("fsc:canonicalOwner", "fsc:ownerRemoved"))
            with self.assertRaisesRegex(mod.Refusal, "ONTOLOGY_TERM_MISSING"):
                mod.qualify(root)
        finally: td.cleanup()

    def test_source_change_changes_receipt_identity(self):
        td, root = self.fixture()
        try:
            before = mod.qualify(root)
            p = root / "ontology/fleet-semantic-closure.ttl"
            p.write_text(p.read_text() + "\n# semantically inert provenance note\n")
            after = mod.qualify(root)
            self.assertNotEqual(before["closure_digest"], after["closure_digest"])
        finally: td.cleanup()

if __name__ == "__main__":
    unittest.main()
