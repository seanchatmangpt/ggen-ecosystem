from pathlib import Path
def test_problem_domain_link():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(:domain ggen-ecosystem-instrument-gain)' in t
