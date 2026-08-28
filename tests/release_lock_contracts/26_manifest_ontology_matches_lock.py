import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];m=tomllib.loads((r/'ggen.toml').read_text());l=tomllib.loads((r/'ecosystem.lock.toml').read_text())
assert m['ontology']['source']==l['manufacturing']['ontology']
