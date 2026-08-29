from support import load_module

def test_git_action_binds_doctor_observation():
    assert load_module().SAFE_ACTIONS[0].observation_ref == "doctor.sh:1-submodules"
