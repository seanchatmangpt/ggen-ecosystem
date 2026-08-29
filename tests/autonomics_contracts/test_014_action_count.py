from support import load_module

def test_exact_safe_action_count():
    assert len(load_module().SAFE_ACTIONS) == 3
