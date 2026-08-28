from pathlib import Path
def test_predicate_capabilities_bound():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(ggen-capabilities-bound)' in t
