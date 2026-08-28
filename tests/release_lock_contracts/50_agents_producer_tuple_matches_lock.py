import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];l=tomllib.loads((r/'ecosystem.lock.toml').read_text());a=(r/'AGENTS.md').read_text()
assert l['ggen']['release'] in a and l['ggen']['commit_sha'] in a and l['ggen_marketplace']['sha'] in a
