from support import Ledger, load_module


def test_failure_receipt_is_blocked():
    """A real non-zero-exit subprocess must produce a BLOCKED receipt.

    Chicago style: no subprocess.run double.  We build a real SafeAction whose
    argv is a real command that really exits 2 (`sh -c 'exit 2'`), let
    admit_and_execute really spawn it, and assert on the real resulting
    ledger state.
    """
    m, ledger = load_module(), Ledger("memory")
    template = m.SAFE_ACTIONS[0]
    failing = m.SafeAction(
        semantic_id=template.semantic_id,
        capability_ref=template.capability_ref,
        argv=["sh", "-c", "exit 2"],
        effect_predicate=template.effect_predicate,
        observer_ref=template.observer_ref,
        observation_ref=template.observation_ref,
        gate=template.gate,
    )
    rc = m.admit_and_execute(failing, ledger)
    assert rc != 0
    assert len(ledger.items) == 1
    assert ledger.items[0].standing == "BLOCKED"
