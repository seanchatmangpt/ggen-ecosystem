import inspect
from support import load_module

def test_ledger_is_repo_confined():
    source = inspect.getsource(load_module().main)
    assert 'REPO_ROOT / "receipts" / "gymact-autonomics-ledger.sqlite3"' in source
