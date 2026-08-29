from support import load_module

def test_docker_argv_is_local_test_build():
    assert load_module().SAFE_ACTIONS[2].argv == ["docker", "build", "-t", "ggen-ecosystem:test", "."]
