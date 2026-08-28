from pathlib import Path
def test_receipt_plan_hash():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-solution.receipt').read_text(); assert 'plan_sha256=3842af99620fc31df21702f55d28cdf09683ef53eea04824a178d746fa72aeca' in t
