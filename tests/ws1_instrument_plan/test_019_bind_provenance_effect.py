from pathlib import Path
def test_bind_provenance_effect():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':effect (provenance-bound)' in t
