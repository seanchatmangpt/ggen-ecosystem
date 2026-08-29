from support import load_module

def test_definition_binds_effect_predicate():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().expected_effects[0].predicate == "submodules_initialized_and_current"
