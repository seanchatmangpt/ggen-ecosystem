#!/usr/bin/env python3
"""Repository-local consistency checks for ecosystem.lock.toml.

These tests intentionally verify identities and evidence standing only. They do not
attempt network publication or actuation.
"""

from __future__ import annotations

import pathlib
import subprocess
import tomllib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
LOCK_PATH = ROOT / "ecosystem.lock.toml"


def gitlink(path: str) -> str:
    output = subprocess.check_output(
        ["git", "ls-tree", "HEAD", path], cwd=ROOT, text=True
    ).strip()
    if not output:
        raise AssertionError(f"missing gitlink: {path}")
    mode, obj_type, sha, observed_path = output.split(maxsplit=3)
    if mode != "160000" or obj_type != "commit" or observed_path != path:
        raise AssertionError(f"not a gitlink: {output}")
    return sha


class EcosystemLockConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with LOCK_PATH.open("rb") as handle:
            cls.lock = tomllib.load(handle)

    def test_ggen_gitlink_matches_lock(self) -> None:
        submodules = self.lock["submodules"]
        self.assertEqual(gitlink(submodules["ggen_path"]), submodules["ggen_commit"])

    def test_marketplace_gitlink_matches_lock(self) -> None:
        submodules = self.lock["submodules"]
        self.assertEqual(
            gitlink(submodules["ggen_marketplace_path"]),
            submodules["ggen_marketplace_commit"],
        )

    def test_autofde_lab_gitlink_matches_lock(self) -> None:
        submodules = self.lock["submodules"]
        self.assertEqual(
            gitlink(submodules["autofde_lab_path"]),
            submodules["autofde_lab_commit"],
        )

    def test_wasm4pm_gitlink_matches_lock(self) -> None:
        submodules = self.lock["submodules"]
        self.assertEqual(
            gitlink(submodules["wasm4pm_path"]),
            submodules["wasm4pm_commit"],
        )

    def test_blocked_capsule_is_not_claimed_available(self) -> None:
        container = self.lock["container"]
        if container.get("requires_republish"):
            self.assertEqual(container.get("standing"), "BLOCKED")
            self.assertTrue(container.get("failure"))

    def test_dated_catalog_is_not_promoted_to_alive(self) -> None:
        catalog = self.lock["catalog"]
        self.assertEqual(catalog.get("standing"), "PARTIAL_ALIVE")
        self.assertTrue(catalog.get("observation_scope", "").startswith("owner-census-"))


if __name__ == "__main__":
    unittest.main()
