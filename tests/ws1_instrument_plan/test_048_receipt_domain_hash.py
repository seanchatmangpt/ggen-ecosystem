from pathlib import Path
def test_receipt_domain_hash():
 t=(Path(__file__).resolve().parents[2]/'planning/instrument-gain-solution.receipt').read_text(); assert 'domain_sha256=a2a9aef68d8b062d6cf7f9e857dc677609fae00296e5b873aded777e19695d09' in t
