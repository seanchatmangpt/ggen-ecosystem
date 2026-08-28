from datetime import datetime
from pathlib import Path
import tomllib
r=Path(__file__).resolve().parents[2]
d=tomllib.loads((r/'ecosystem.lock.toml').read_text())
datetime.fromisoformat(d['updated_at'].replace('Z','+00:00'))
