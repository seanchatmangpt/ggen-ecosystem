from support import Ledger, load_module


def test_success_receipt_is_verified():
    """Real subprocess, real exit code, real receipt state.

    Instead of faking subprocess.run, this runs the real `/usr/bin/true`
    binary through admit_and_execute's real execution path, so
    receipt.verified is derived from an actual process exit status.
    """
    m, ledger = load_module(), Ledger("memory")
    template = m.SAFE_ACTIONS[0]
    action = m.SafeAction(
        semantic_id=template.semantic_id,
        capability_ref=template.capability_ref,
        argv=["true"],
        effect_predicate=template.effect_predicate,
        observer_ref=template.observer_ref,
        observation_ref=template.observation_ref,
        gate=template.gate,
    )
    assert m.admit_and_execute(action, ledger) == 0
    assert ledger.items[0].verified is True
    assert ledger.items[0].reason == "exit_code=0"
