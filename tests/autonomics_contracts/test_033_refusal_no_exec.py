import tempfile
from pathlib import Path

from support import Ledger, load_module


def test_refusal_does_not_execute():
    m = load_module(admitted=False)
    with tempfile.TemporaryDirectory() as tmp:
        sentinel = Path(tmp) / "executed.sentinel"
        # Real subprocess argv: if admit_and_execute ever reaches subprocess.run,
        # this shell command really creates the sentinel file on disk.
        action = m.SafeAction(
            semantic_id="contract.refusal.no_exec",
            capability_ref="contract.no_exec",
            argv=["sh", "-c", f"touch {sentinel}"],
            effect_predicate="sentinel_written",
            observer_ref="fs.stat",
            observation_ref="contract:033",
            gate="contract-033",
        )
        assert m.admit_and_execute(action, Ledger("memory")) == 1
        assert not sentinel.exists(), "refused action still executed its argv"
