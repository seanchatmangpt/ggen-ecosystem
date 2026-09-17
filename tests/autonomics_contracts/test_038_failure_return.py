from support import Ledger, load_module


def test_failure_returns_one():
    """Real subprocess: a shell command that writes to stderr and exits 7."""
    m = load_module()
    template = m.SAFE_ACTIONS[0]
    failing = m.SafeAction(
        semantic_id=template.semantic_id,
        capability_ref=template.capability_ref,
        argv=["sh", "-c", "echo boom >&2; exit 7"],
        effect_predicate=template.effect_predicate,
        observer_ref=template.observer_ref,
        observation_ref=template.observation_ref,
        gate=template.gate,
    )
    ledger = Ledger("memory")
    assert m.admit_and_execute(failing, ledger) == 1
    assert len(ledger.items) == 1
    assert ledger.items[0].standing == m.gymact.Standing.BLOCKED
