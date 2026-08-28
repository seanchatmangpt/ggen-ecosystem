from pathlib import Path
def test_plan_step_5():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-plan.txt').read_text(); assert '5: (merge-ecosystem-pr)' in t
