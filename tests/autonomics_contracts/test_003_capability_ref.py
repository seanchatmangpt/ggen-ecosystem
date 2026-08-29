from support import load_module

def test_definition_retains_capability():
    m = load_module()
    assert m.SAFE_ACTIONS[2].build_definition().capability_ref == "docker.build"
