import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];d=tomllib.loads((r/'ecosystem.lock.toml').read_text());c=d['catalog']
assert c['observed_total_owned_repositories']==c['observed_public_repositories']+c['observed_private_repositories']
