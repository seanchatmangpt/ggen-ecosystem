from support import Ledger, load_module

def test_refusal_returns_one():
    m = load_module(admitted=False)
    assert m.admit_and_execute(m.SAFE_ACTIONS[0], Ledger("memory")) == 1
