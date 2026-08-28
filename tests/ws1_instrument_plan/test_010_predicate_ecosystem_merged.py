from pathlib import Path
def test_predicate_ecosystem_merged():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(ecosystem-merged)' in t
