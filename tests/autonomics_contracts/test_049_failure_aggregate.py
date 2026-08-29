import inspect
from support import load_module

def test_failure_aggregate_returns_nonzero():
    source = inspect.getsource(load_module().main)
    assert "return 0 if all(c == 0 for c in exit_codes) else 1" in source
