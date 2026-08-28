from pathlib import Path
def test_receipt_optimality():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-solution.receipt').read_text(); assert 'optimality=unit-cost-shortest-plan' in t
