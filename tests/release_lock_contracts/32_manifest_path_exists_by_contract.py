import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];l=tomllib.loads((r/'ecosystem.lock.toml').read_text())
assert (r/l['manufacturing']['manifest']).is_file()
