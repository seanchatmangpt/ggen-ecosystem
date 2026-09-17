from support import Ledger, load_module


def test_executed_receipt_records_world_change():
    """Real subprocess execution: `true` is a real program on this platform,
    so the module's own subprocess.run runs for real and the receipt records
    the real world_changed/verified state derived from a real exit code."""
    m, ledger = load_module(), Ledger("memory")
    action = m.SafeAction(
        semantic_id="ggen-ecosystem.contract.noop_true",
        capability_ref="shell.true",
        argv=["true"],
        effect_predicate="noop_completed",
        observer_ref="shell.exit_code",
        observation_ref="contract:041",
        gate="contract-041",
    )
    m.admit_and_execute(action, ledger)
    assert ledger.items[0].world_changed is True
    assert ledger.items[0].verified is True
    assert ledger.items[0].reason == "exit_code=0"
