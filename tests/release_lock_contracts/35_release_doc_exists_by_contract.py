from pathlib import Path
r=Path(__file__).resolve().parents[2]
assert (r/'docs'/'RELEASE.md').is_file()
