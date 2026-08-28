from pathlib import Path
def test_predicate_base_current():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(ecosystem-base-current)' in t
