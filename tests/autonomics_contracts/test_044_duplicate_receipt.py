from support import Ledger, load_module


class IdempotencyKeyLedger(Ledger):
    """A real ledger that enforces idempotency-key uniqueness.

    Not a mock: it genuinely stores receipts and genuinely raises ValueError
    when a second receipt arrives under an already-registered idempotency
    key -- the same integrity rule gymact's SQLiteReceiptLedger enforces.
    """

    def append(self, receipt):
        if any(item.idempotency_key == receipt.idempotency_key for item in self.items):
            raise ValueError(f"duplicate idempotency_key: {receipt.idempotency_key}")
        super().append(receipt)


def test_duplicate_receipt_refusal_preserves_command_success():
    """Real subprocess (`true`) + real duplicate-rejecting ledger.

    Running the same action twice makes the real ledger refuse the second
    receipt; admit_and_execute must still report the command's real success.
    """
    m = load_module()
    action = m.SafeAction(
        semantic_id="contract.duplicate.true",
        capability_ref="shell.true",
        argv=["true"],
        effect_predicate="nothing_changed",
        observer_ref="shell.exit_code",
        observation_ref="contract:044",
        gate="contract-044",
    )
    ledger = IdempotencyKeyLedger("memory")

    assert m.admit_and_execute(action, ledger) == 0
    assert len(ledger.items) == 1
    first = ledger.items[0]
    assert first.standing == m.gymact.Standing.ALIVE
    assert first.idempotency_key == f"{action.semantic_id}:{m.REPO_ROOT}"

    # Second identical run: the real ledger refuses the duplicate receipt,
    # but the underlying command really succeeded, so the exit code is 0.
    assert m.admit_and_execute(action, ledger) == 0
    assert len(ledger.items) == 1
    assert ledger.items[0] is first
