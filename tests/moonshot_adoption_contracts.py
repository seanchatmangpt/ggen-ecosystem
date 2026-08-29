#!/usr/bin/env python3
"""Contract tests for public-adoption moonshot guards."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ecosystem_alive", ROOT / "scripts" / "ecosystem_alive.py")
assert SPEC and SPEC.loader
alive = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(alive)


class MoonshotAdoptionContracts(unittest.TestCase):
    def test_capsule_requires_immutable_digest(self) -> None:
        result = alive.admit_capsule_identity("ghcr.io/acme/app:latest", available=True)
        self.assertEqual(result["standing"], "REFUSED[MUTABLE_CAPSULE_IDENTITY]")

    def test_unavailable_digest_is_typed_refusal(self) -> None:
        digest = "a" * 64
        result = alive.admit_capsule_identity(f"ghcr.io/acme/app@sha256:{digest}", available=False)
        self.assertEqual(result["standing"], "REFUSED[CAPSULE_IDENTITY_UNAVAILABLE]")

    def test_available_digest_is_admitted(self) -> None:
        digest = "b" * 64
        result = alive.admit_capsule_identity(f"ghcr.io/acme/app@sha256:{digest}", available=True)
        self.assertEqual(result["standing"], "ALIVE")

    def test_generated_only_workflow_patch_is_refused(self) -> None:
        result = alive.admit_projection_change([".github/workflows/ggen-ecosystem-sync.yml"])
        self.assertEqual(result["standing"], "REFUSED[GENERATED_PROJECTION_DIRECT_EDIT]")

    def test_semantic_source_plus_projection_is_admitted(self) -> None:
        result = alive.admit_projection_change(["ontology.ttl", ".github/workflows/ggen-ecosystem-sync.yml"])
        self.assertEqual(result["standing"], "ALIVE")

    def test_host_path_is_canonical_fallback(self) -> None:
        result = alive.select_consumer_execution(container_available=False, host_available=True)
        self.assertEqual(result, {"standing": "ALIVE", "route": "host"})

    def test_no_execution_surface_is_typed_unsupported(self) -> None:
        result = alive.select_consumer_execution(container_available=False, host_available=False)
        self.assertEqual(result["standing"], "UNSUPPORTED[NO_CONSUMER_EXECUTION_SURFACE]")


if __name__ == "__main__":
    unittest.main()
