from pathlib import Path
def test_predicate_capability_admitted():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(capability-vocabulary-admitted)' in t
