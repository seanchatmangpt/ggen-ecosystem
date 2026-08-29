from support import load_module

def test_definition_requires_process_conformance():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().verification.kind == "PROCESS_CONFORMANCE"
