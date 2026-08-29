from support import load_module

def test_ggen_action_uses_drift_gate():
    assert load_module().SAFE_ACTIONS[1].gate == "9-workflow-drift"
