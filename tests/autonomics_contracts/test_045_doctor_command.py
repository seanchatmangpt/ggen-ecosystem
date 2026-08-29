import inspect
from support import load_module

def test_main_observes_doctor_json():
    source = inspect.getsource(load_module().main)
    assert '["bash", str(REPO_ROOT / "scripts" / "doctor.sh"), "--json"]' in source
