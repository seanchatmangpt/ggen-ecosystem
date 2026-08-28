from pathlib import Path
def test_predicate_pr_open():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-domain.ppddl').read_text(); assert '(ecosystem-pr-open)' in t
