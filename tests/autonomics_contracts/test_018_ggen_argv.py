from support import load_module

def test_ggen_argv_is_sync_run():
    assert load_module().SAFE_ACTIONS[1].argv == ["ggen", "sync", "run"]
