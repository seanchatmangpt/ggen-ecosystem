from types import SimpleNamespace
from support import Ledger, load_module

def test_duplicate_receipt_refusal_preserves_command_success(monkeypatch):
    m, ledger = load_module(), Ledger("memory")
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=0, stderr=""))
    monkeypatch.setattr(ledger, "append", lambda receipt: (_ for _ in ()).throw(ValueError("duplicate")))
    assert m.admit_and_execute(m.SAFE_ACTIONS[0], ledger) == 0
