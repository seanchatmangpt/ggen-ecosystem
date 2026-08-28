from pathlib import Path
def test_plan_step_3():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-plan.txt').read_text(); assert '3: (record-ppddl-plan)' in t
