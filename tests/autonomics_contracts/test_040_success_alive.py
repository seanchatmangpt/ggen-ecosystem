"""Contract: a really-succeeding subprocess yields an ALIVE receipt standing.

Chicago style: no subprocess double.  admit_and_execute runs a REAL
subprocess (/usr/bin/true, exit 0) in the real repo root, and the assertion
is on the real receipt state the real code path appended to the ledger.
"""
from support import Ledger, load_module


def test_success_receipt_is_alive():
    m = load_module()
    ledger = Ledger("memory")
    action = m.SafeAction(
        semantic_id="ggen-ecosystem.contract.always_succeeds",
        capability_ref="shell.true",
        argv=["true"],
        effect_predicate="process_exited_zero",
        observer_ref="shell.exit_status",
        observation_ref="contract:040",
        gate="contract-040",
    )

    rc = m.admit_and_execute(action, ledger)

    assert rc == 0
    assert len(ledger.items) == 1
    assert ledger.items[0].standing == "ALIVE"
