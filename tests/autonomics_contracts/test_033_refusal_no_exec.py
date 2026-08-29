from support import Ledger, load_module

def test_refusal_does_not_execute(monkeypatch):
    m = load_module(admitted=False)
    monkeypatch.setattr(m.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("executed")))
    assert m.admit_and_execute(m.SAFE_ACTIONS[0], Ledger("memory")) == 1
