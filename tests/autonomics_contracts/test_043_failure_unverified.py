from types import SimpleNamespace
from support import Ledger, load_module

def test_failure_receipt_is_unverified(monkeypatch):
    m, ledger = load_module(), Ledger("memory")
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1, stderr=""))
    m.admit_and_execute(m.SAFE_ACTIONS[0], ledger)
    assert ledger.items[0].verified is False
