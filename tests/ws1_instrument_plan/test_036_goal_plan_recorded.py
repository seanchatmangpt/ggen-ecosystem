from pathlib import Path
def test_goal_plan_recorded():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-problem.ppddl').read_text(); assert '(ppddl-plan-recorded)' in t[t.index('(:goal'):]
