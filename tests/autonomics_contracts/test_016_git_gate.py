from support import load_module

def test_git_action_uses_submodule_gate():
    assert load_module().SAFE_ACTIONS[0].gate == "1-submodules"
