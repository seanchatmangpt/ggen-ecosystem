from support import load_module

def test_gate_standing_ignores_non_objects():
    assert load_module().gate_standing({"gates": [None, "x", 3]}, "x") is None
