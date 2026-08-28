import tomllib
from pathlib import Path
r=Path(__file__).resolve().parents[2];d=tomllib.loads((r/'ecosystem.lock.toml').read_text())
assert d['catalog']['census_receipt']=='receipts/github-ecosystem-census-2026-08-28.json'
