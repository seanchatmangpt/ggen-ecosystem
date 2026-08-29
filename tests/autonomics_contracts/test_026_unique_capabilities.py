from support import load_module

def test_action_capabilities_are_unique():
    actions = load_module().SAFE_ACTIONS
    assert len({a.capability_ref for a in actions}) == len(actions)
