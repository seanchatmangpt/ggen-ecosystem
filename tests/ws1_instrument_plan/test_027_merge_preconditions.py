from pathlib import Path
def test_merge_preconditions():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert ':precondition (and (ecosystem-pr-open) (ecosystem-base-current))' in t
