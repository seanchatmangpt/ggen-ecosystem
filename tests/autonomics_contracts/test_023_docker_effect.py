from support import load_module

def test_docker_action_declares_local_substrate():
    assert load_module().SAFE_ACTIONS[2].effect_predicate == "local_container_substrate_built"
