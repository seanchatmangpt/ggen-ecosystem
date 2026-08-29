from support import load_module

def test_definition_admits_no_untyped_input():
    m = load_module()
    assert m.SAFE_ACTIONS[0].build_definition().input_schema == {"type": "object", "properties": {}}
