from support import Ledger, load_module


def test_success_returns_zero():
    """Real subprocess: /usr/bin/true exits 0, so admit_and_execute returns 0."""
    m = load_module()
    action = m.SafeAction(
        semantic_id="contract.success.true",
        capability_ref="shell.true",
        argv=["true"],
        effect_predicate="nothing_changed",
        observer_ref="shell.exit_code",
        observation_ref="contract:037",
        gate="contract-037",
    )
    ledger = Ledger("memory")
    assert m.admit_and_execute(action, ledger) == 0
    assert len(ledger.items) == 1
    assert ledger.items[0].standing == m.gymact.Standing.ALIVE
