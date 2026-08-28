import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];m=tomllib.loads((r/'ggen.toml').read_text());p=Path(m['packs']['github-actions']['subdir']).parts
assert len(p)>=2 and p[0]=='packs' and '..' not in p
