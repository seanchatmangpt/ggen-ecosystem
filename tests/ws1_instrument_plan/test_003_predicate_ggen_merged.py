from pathlib import Path
def test_predicate_ggen_merged():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(ggen-instrument-merged)' in t
