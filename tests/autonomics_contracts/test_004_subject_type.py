from support import load_module

def test_definition_confines_subject_type():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().subject_type == "git_worktree"
