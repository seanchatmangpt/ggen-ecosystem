import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "certify_ecosystem.py"
spec = importlib.util.spec_from_file_location("certify_ecosystem", MODULE_PATH)
cert = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cert)

GGEN = "c61ee99359c9dbc7b3cb71687976932a3e737ed4"
MARKET = "89adf4c8476f7edc8067fdbb1c256cfbfa22df6a"
DIGEST = "sha256:" + "b" * 64
SUBJECT = "e16feba269e9f51676418beacabce48aa7c1b19d"
HEAD = "f42aa25c4974a0d5a701ed0e08f3bce46d69d115"


def valid_lock():
    return {
        "ggen": {"release": "v26.8.28", "commit_sha": GGEN},
        "ggen_marketplace": {"sha": MARKET},
        "submodules": {"ggen_commit": GGEN, "ggen_marketplace_commit": MARKET},
        "container": {
            "repository": "ghcr.io/seanchatmangpt/ggen-ecosystem",
            "tag": "v26.8.28",
            "digest": DIGEST,
        },
    }


def valid_receipt():
    return {
        "subject": {"repository": "seanchatmangpt/ggen-ecosystem", "commit": SUBJECT},
        "ecosystem": {
            "version": "v26.8.28",
            "ggen_commit": GGEN,
            "marketplace_commit": MARKET,
            "container_digest": DIGEST,
        },
        "admission": {"result": "ADMITTED"},
        "execution": {"exit_code": 0},
        "verification": {"doctor": "PARTIAL_ALIVE", "chicago": "ALIVE", "dod": "PARTIAL_ALIVE"},
        "standing": "PARTIAL_ALIVE",
    }


class MfactCertificationTests(unittest.TestCase):
    def test_exact_producer_pins_admit(self):
        self.assertEqual(cert.validate_lock(valid_lock()), [])

    def test_ggen_submodule_drift_refuses(self):
        lock = valid_lock()
        lock["submodules"]["ggen_commit"] = "0" * 40
        self.assertIn("REFUSED[GGEN_SUBMODULE_PIN_DRIFT]", cert.validate_lock(lock))

    def test_mutable_or_placeholder_container_identity_refuses(self):
        lock = valid_lock()
        lock["container"]["digest"] = "UNKNOWN-TODO"
        errors = cert.validate_lock(lock)
        self.assertIn("REFUSED[IMMUTABLE_CONTAINER_DIGEST_REQUIRED]", errors)
        self.assertTrue(any("PLACEHOLDER_LOAD_BEARING_IDENTITY" in error for error in errors))

    def test_receipt_cannot_silently_change_marketplace_subject(self):
        receipt = valid_receipt()
        receipt["ecosystem"]["marketplace_commit"] = "0" * 40
        self.assertIn("REFUSED[RECEIPT_MARKETPLACE_DRIFT]", cert.validate_release_receipt(receipt, valid_lock()))

    def test_historical_release_evidence_cannot_promote_current_head_alive(self):
        standing, reasons = cert.classify_standing(
            "ALIVE",
            git_available=True,
            current_head=HEAD,
            receipt_subject=SUBJECT,
            receipt_subject_ancestor=True,
            load_bearing_changed=False,
        )
        self.assertEqual(standing, "PARTIAL_ALIVE[BOUNDED_CERTIFICATION]")
        self.assertTrue(any("historical" in reason for reason in reasons))

    def test_exact_alive_subject_can_reach_alive(self):
        standing, _ = cert.classify_standing(
            "ALIVE",
            git_available=True,
            current_head=SUBJECT,
            receipt_subject=SUBJECT,
            receipt_subject_ancestor=True,
            load_bearing_changed=False,
        )
        self.assertEqual(standing, "ALIVE")

    def test_partial_receipt_caps_exact_subject(self):
        standing, reasons = cert.classify_standing(
            "PARTIAL_ALIVE",
            git_available=True,
            current_head=SUBJECT,
            receipt_subject=SUBJECT,
            receipt_subject_ancestor=True,
            load_bearing_changed=False,
        )
        self.assertEqual(standing, "PARTIAL_ALIVE[BOUNDED_CERTIFICATION]")
        self.assertTrue(any("PARTIAL_ALIVE" in reason for reason in reasons))

    def test_generated_projection_cannot_be_standing_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ontology.ttl").write_text("# source\n", encoding="utf-8")
            (root / "generated.yml").write_text("name: generated\n", encoding="utf-8")
            ledger = {
                "artifact": [
                    {
                        "path": "generated.yml",
                        "kind": "projection",
                        "producer": "ggen",
                        "source": "ontology.ttl",
                        "standing_authority": True,
                        "load_bearing": True,
                    }
                ]
            }
            errors, _ = cert.validate_ledger(root, ledger)
            self.assertIn("REFUSED[GENERATED_PROJECTION_STANDING_AUTHORITY]:generated.yml", errors)


if __name__ == "__main__":
    unittest.main()
