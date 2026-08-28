from __future__ import annotations

import re
import tomllib
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = tomllib.loads((ROOT / "ecosystem.lock.toml").read_text())
MANIFEST = tomllib.loads((ROOT / "ggen.toml").read_text())
AGENTS = (ROOT / "AGENTS.md").read_text()
RELEASE = (ROOT / "docs" / "RELEASE.md").read_text()

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
GGEN_RELEASE = re.compile(r"^v\d+\.\d+\.\d+(?:[.+-][0-9A-Za-z.-]+)?$")


class ReleaseLockContracts(unittest.TestCase):

    def test_lock_schema_version(self):
        self.assertEqual(LOCK["version"], 2)


if __name__ == "__main__":
    unittest.main()
