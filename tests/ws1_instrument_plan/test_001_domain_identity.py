from pathlib import Path


def test_domain_identity():
    text = (Path(__file__).resolve().parents[2] / "planning/instrument-gain-domain.ppddl").read_text()
    assert "(define (domain ggen-ecosystem-instrument-gain)" in text
