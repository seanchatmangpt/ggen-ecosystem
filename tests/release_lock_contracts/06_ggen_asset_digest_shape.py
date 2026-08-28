import re,tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2]; d=tomllib.loads((r/'ecosystem.lock.toml').read_text())
assert re.fullmatch(r'[0-9a-f]{64}',d['ggen']['linux_x86_64_asset_sha256'])
