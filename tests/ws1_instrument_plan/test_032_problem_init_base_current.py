from pathlib import Path
def test_problem_init_base_current():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(ecosystem-base-current))' in t
