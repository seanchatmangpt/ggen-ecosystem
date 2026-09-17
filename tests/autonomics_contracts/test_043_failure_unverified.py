from support import Ledger, load_module


def test_failure_receipt_is_unverified():
    """A really-failing command must produce a receipt with verified=False.

    Chicago style: no subprocess double. `false` is a real executable that
    really exits 1, so admit_and_execute runs the real subprocess path and
    the assertion is on the real persisted receipt state.
    """
    m, ledger = load_module(), Ledger("memory")
    failing = m.SafeAction(
        semantic_id="ggen-ecosystem.contract.always_failing_command",
        capability_ref="shell.false",
        argv=["false"],
        effect_predicate="never_satisfied",
        observer_ref="shell.exit_code",
        observation_ref="contract:043",
        gate="contract-043",
    )
    rc = m.admit_and_execute(failing, ledger)
    assert rc == 1
    assert ledger.items[0].verified is False
    assert ledger.items[0].reason == "exit_code=1"
