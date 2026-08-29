from support import load_module

def test_gate_standing_returns_none_when_absent():
    assert load_module().gate_standing({"gates": []}, "x") is None
