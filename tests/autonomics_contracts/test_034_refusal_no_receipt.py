from support import Ledger, load_module

def test_refusal_writes_no_receipt():
    m, ledger = load_module(admitted=False), Ledger("memory")
    m.admit_and_execute(m.SAFE_ACTIONS[0], ledger)
    assert ledger.items == []
