from support import load_module

def test_docker_action_uses_image_gate():
    assert load_module().SAFE_ACTIONS[2].gate == "4-docker-image"
