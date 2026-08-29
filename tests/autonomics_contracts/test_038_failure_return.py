from types import SimpleNamespace
from support import Ledger, load_module

def test_failure_returns_one(monkeypatch):
    m = load_module()
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=7, stderr="boom"))
    assert m.admit_and_execute(m.SAFE_ACTIONS[0], Ledger("memory")) == 1
