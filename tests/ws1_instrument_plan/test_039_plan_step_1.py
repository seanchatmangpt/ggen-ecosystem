from pathlib import Path
def test_plan_step_1():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-plan.txt').read_text(); assert '1: (bind-ggen-capabilities)' in t
