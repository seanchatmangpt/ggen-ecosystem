from pathlib import Path
def test_publish_effect():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':effect (ecosystem-pr-open)' in t
