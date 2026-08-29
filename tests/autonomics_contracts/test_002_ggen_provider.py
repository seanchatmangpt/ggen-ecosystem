from support import load_module

def test_ggen_action_uses_shell_provider():
    m = load_module()
    assert m.SAFE_ACTIONS[1].build_definition().provider_ref == "shell"
