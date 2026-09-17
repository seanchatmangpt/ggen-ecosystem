from support import Ledger, load_module


def test_success_appends_receipt():
    """Real subprocess execution: `true` is a real, cheap, non-destructive
    command that really exits 0, so the receipt is produced by the module's
    real subprocess.run call rather than a faked one."""
    m, ledger = load_module(), Ledger("memory")
    action = m.SafeAction(
        semantic_id="ggen-ecosystem.contract.always_succeeds",
        capability_ref="shell.true",
        argv=["true"],
        effect_predicate="nothing_changed",
        observer_ref="shell.exit_code",
        observation_ref="contract:036",
        gate="contract-036",
    )
    exit_code = m.admit_and_execute(action, ledger)
    assert exit_code == 0
    assert len(ledger.items) == 1
    receipt = ledger.items[0]
    assert receipt.capability_ref == "shell.true"
    assert receipt.standing == "ALIVE"
    assert receipt.verified is True
    assert receipt.reason == "exit_code=0"
