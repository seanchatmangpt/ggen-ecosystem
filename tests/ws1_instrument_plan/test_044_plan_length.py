from pathlib import Path
def test_plan_length():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-plan.txt').read_text(); assert '; length = 6' in t
