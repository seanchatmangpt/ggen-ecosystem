from support import load_module

def test_definition_binds_observer():
    m = load_module()
    assert m.SAFE_ACTIONS[1].build_definition().verification.observer_ref == "ggen.sync.dry_run_decisions"
