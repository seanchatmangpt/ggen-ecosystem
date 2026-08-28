import re,tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2]; d=tomllib.loads((r/'ecosystem.lock.toml').read_text())
assert re.fullmatch(r'[0-9a-f]{40}',d['ggen_marketplace']['sha'])
