from support import load_module

def test_safe_set_excludes_authority_publish():
    forbidden = {"docker.push", "github.release", "git.push"}
    assert forbidden.isdisjoint({a.capability_ref for a in load_module().SAFE_ACTIONS})
