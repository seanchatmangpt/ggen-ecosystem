from support import load_module

def test_gate_standing_handles_missing_collection():
    assert load_module().gate_standing({}, "x") is None
