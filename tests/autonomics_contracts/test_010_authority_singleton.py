from support import load_module

def test_definition_requests_only_its_capability():
    m = load_module()
    assert m.SAFE_ACTIONS[1].build_definition().authority.capability_refs == ("ggen.sync.run",)
