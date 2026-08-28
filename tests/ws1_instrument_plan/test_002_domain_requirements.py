from pathlib import Path

def test_domain_requirements():
    text=(Path(__file__).resolve().parents[2]/"planning/instrument-gain-domain.ppddl").read_text()
    assert "(:requirements :strips)" in text
