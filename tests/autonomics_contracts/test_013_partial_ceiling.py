from support import load_module

def test_definition_starts_partial_alive():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().standing == "PARTIAL_ALIVE"
