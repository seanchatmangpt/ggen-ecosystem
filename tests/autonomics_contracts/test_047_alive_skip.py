import inspect
from support import load_module

def test_alive_gate_skips_execution():
    source = inspect.getsource(load_module().main)
    assert 'if standing == "ALIVE"' in source and "continue" in source
