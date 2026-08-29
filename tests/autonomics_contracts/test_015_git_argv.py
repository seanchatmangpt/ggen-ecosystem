from support import load_module

def test_git_argv_is_recursive_init():
    assert load_module().SAFE_ACTIONS[0].argv == ["git", "submodule", "update", "--init", "--recursive"]
