from pathlib import Path
def test_admit_preconditions():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':precondition (and (ggen-instrument-merged) (ecosystem-base-current))' in t
