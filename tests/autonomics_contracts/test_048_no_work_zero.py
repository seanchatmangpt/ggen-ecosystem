import inspect
from support import load_module

def test_no_admitted_work_returns_zero():
    source = inspect.getsource(load_module().main)
    assert "if not exit_codes" in source and "return 0" in source
