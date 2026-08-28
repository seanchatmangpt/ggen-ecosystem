from pathlib import Path
def test_goal_ecosystem_merged():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(ecosystem-merged)' in t[t.index('(:goal'):]
