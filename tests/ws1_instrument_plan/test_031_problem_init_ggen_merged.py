from pathlib import Path
def test_problem_init_ggen_merged():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(:init\n    (ggen-instrument-merged)' in t
