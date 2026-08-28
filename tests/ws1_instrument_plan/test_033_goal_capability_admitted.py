from pathlib import Path
def test_goal_capability_admitted():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(capability-vocabulary-admitted)' in t[t.index('(:goal'):]
