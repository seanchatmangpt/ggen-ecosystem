from pathlib import Path
def test_receipt_problem_hash():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-solution.receipt').read_text(); assert 'problem_sha256=05301a9bedd666e3f2dc798c531642a32fd10e8a343b665332ecd2beea72a469' in t
