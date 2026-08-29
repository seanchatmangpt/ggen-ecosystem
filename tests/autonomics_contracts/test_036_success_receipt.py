from types import SimpleNamespace
from support import Ledger, load_module

def test_success_appends_receipt(monkeypatch):
    m, ledger = load_module(), Ledger("memory")
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stderr=""))
    m.admit_and_execute(m.SAFE_ACTIONS[0], ledger)
    assert len(ledger.items) == 1
