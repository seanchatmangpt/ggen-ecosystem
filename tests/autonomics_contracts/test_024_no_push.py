from support import load_module

def test_safe_set_contains_no_push():
    assert all("push" not in action.argv for action in load_module().SAFE_ACTIONS)
