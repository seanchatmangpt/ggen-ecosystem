from pathlib import Path
def test_predicate_provenance_bound():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(provenance-bound)' in t
