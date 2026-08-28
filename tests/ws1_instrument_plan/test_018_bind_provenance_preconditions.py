from pathlib import Path
def test_bind_provenance_preconditions():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':precondition (and (ggen-capabilities-bound) (ggen-instrument-merged))' in t
