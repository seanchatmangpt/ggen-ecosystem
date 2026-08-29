from support import load_module

def test_gate_standing_returns_match():
    m = load_module()
    assert m.gate_standing({"gates": [{"gate": "x", "standing": "ALIVE"}]}, "x") == "ALIVE"
