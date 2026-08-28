from pathlib import Path
def test_plan_step_2():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-plan.txt').read_text(); assert '2: (bind-provenance)' in t
