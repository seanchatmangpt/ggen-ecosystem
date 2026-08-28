import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];d=tomllib.loads((r/'ggen.toml').read_text())
assert d['project']['name']=='ggen-ecosystem'
