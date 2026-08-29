from support import load_module

def test_action_ids_are_unique():
    actions = load_module().SAFE_ACTIONS
    assert len({a.semantic_id for a in actions}) == len(actions)
