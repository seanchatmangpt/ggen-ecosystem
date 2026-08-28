from pathlib import Path
def test_goal_capabilities_bound():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(ggen-capabilities-bound)' in t[t.index('(:goal'):]
