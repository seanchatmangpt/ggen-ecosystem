from types import SimpleNamespace
from support import Ledger, load_module

def test_success_returns_zero(monkeypatch):
    m = load_module()
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stderr=""))
    assert m.admit_and_execute(m.SAFE_ACTIONS[0], Ledger("memory")) == 0
