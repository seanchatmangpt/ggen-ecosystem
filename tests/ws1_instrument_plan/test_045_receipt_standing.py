from pathlib import Path
def test_receipt_standing():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-solution.receipt').read_text(); assert 'standing=PARTIAL_ALIVE' in t
