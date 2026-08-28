from pathlib import Path
def test_plan_step_4():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-plan.txt').read_text(); assert '4: (publish-ecosystem-pr)' in t
