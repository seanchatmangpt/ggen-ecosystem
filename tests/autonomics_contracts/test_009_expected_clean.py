from support import load_module

def test_definition_requires_clean_observation():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().verification.expected == {"clean": True}
