from support import load_module

def test_definition_is_reversible():
    m = load_module()
    assert m.SAFE_ACTIONS[2].build_definition().reversal == "REVERSIBLE"
