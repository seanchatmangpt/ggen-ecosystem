from support import load_module

def test_git_action_uses_git_provider():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().provider_ref == "git"
