from types import SimpleNamespace
from support import Ledger, load_module

def test_success_receipt_is_alive(monkeypatch):
    m, ledger = load_module(), Ledger("memory")
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stderr=""))
    m.admit_and_execute(m.SAFE_ACTIONS[0], ledger)
    assert ledger.items[0].standing == "ALIVE"
