from support import load_module

def test_ggen_action_declares_regeneration_effect():
    assert load_module().SAFE_ACTIONS[1].effect_predicate == "workflow_projections_regenerated"
