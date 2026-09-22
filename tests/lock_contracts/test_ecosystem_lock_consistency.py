#!/usr/bin/env python3
"""Repository-local consistency checks for ecosystem.lock.toml.

These tests intentionally verify identities and evidence standing only. They do not
attempt network publication or actuation.
"""

from __future__ import annotations

import pathlib
import re
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


def mix_version(path: pathlib.Path) -> str:
    text = path.read_text()
    match = re.search(r'@version\s+"([^"]+)"', text) or re.search(
        r'version:\s*"([^"]+)"', text
    )
    if not match:
        raise AssertionError(f"no Mix project version found in {path}")
    return match.group(1)


def cargo_workspace_version(path: pathlib.Path) -> str:
    with path.open("rb") as handle:
        doc = tomllib.load(handle)
    return doc["workspace"]["package"]["version"]


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

    def test_ggen_toml_packs_comment_marketplace_sha_matches_lock(self) -> None:
        """Tripwire for the comment-vs-pin drift class fixed in #248/#263/#266/#267.

        Any 40-hex commit SHA cited in a ggen.toml comment must be the pinned
        marketplace commit; a stale citation must fail here rather than mislead
        about which commit is actually vendored.
        """
        manifest_text = (ROOT / "ggen.toml").read_text()
        comment_lines = [
            line for line in manifest_text.splitlines() if line.lstrip().startswith("#")
        ]
        cited_shas = set(
            re.findall(r"\b[0-9a-f]{40}\b", "\n".join(comment_lines))
        )
        pinned = self.lock["submodules"]["ggen_marketplace_commit"]
        self.assertEqual(
            cited_shas,
            {pinned},
            msg=(
                "ggen.toml comment cites marketplace SHA(s) "
                f"{sorted(cited_shas)} but ecosystem.lock.toml pins {pinned} "
                "-- update the comment when the submodule pin moves"
            ),
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


    def test_ggen_release_matches_vendored_workspace_version(self) -> None:
        version = cargo_workspace_version(ROOT / "vendor/ggen/Cargo.toml")
        self.assertEqual(self.lock["ggen"]["release"], f"v{version}")

    def test_ggen_igniter_version_and_gitlink_match_lock(self) -> None:
        submodules = self.lock["submodules"]
        self.assertEqual(
            gitlink(submodules["ggen_igniter_path"]),
            submodules["ggen_igniter_commit"],
        )
        self.assertEqual(
            self.lock["ggen_igniter"]["version"],
            mix_version(ROOT / submodules["ggen_igniter_path"] / "mix.exs"),
        )

    def test_beam4pm_version_and_gitlink_match_lock(self) -> None:
        submodules = self.lock["submodules"]
        self.assertEqual(
            gitlink(submodules["beam4pm_path"]),
            submodules["beam4pm_commit"],
        )
        self.assertEqual(
            self.lock["beam4pm"]["version"],
            mix_version(ROOT / submodules["beam4pm_path"] / "mix.exs"),
        )

    def test_wasm4pm_version_matches_vendored_workspace_version(self) -> None:
        submodules = self.lock["submodules"]
        version = cargo_workspace_version(
            ROOT / submodules["wasm4pm_path"] / "Cargo.toml"
        )
        self.assertEqual(self.lock["wasm4pm"]["version"], version)

    def test_recent_version_snapshot_matches_direct_composition_versions(self) -> None:
        recent = self.lock["recent_versions"]
        self.assertEqual(recent["ggen"]["version"], self.lock["ggen"]["release"].removeprefix("v"))
        self.assertEqual(recent["ggen_igniter"]["version"], self.lock["ggen_igniter"]["version"])
        self.assertEqual(recent["beam4pm"]["version"], self.lock["beam4pm"]["version"])
        self.assertEqual(recent["wasm4pm"]["version"], self.lock["wasm4pm"]["version"])

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
