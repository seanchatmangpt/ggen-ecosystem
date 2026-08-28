from pathlib import Path
r=Path(__file__).resolve().parents[2];t=(r/'docs'/'RELEASE.md').read_text()
assert 'admitted repository/pack closure' in t
