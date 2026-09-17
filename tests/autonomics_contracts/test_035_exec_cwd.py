"""Execution is confined to REPO_ROOT -- proven by a real subprocess.

Chicago style: no fake for `subprocess.run`.  A real SafeAction whose argv is a
real shell command records its own real working directory to a real file on
disk; the assertion is on that recorded state, not on captured kwargs.
"""
import tempfile
from pathlib import Path

from support import Ledger, load_module


def test_execution_is_repo_confined():
    m = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "cwd.txt"
        action = m.SafeAction(
            semantic_id="ggen-ecosystem.contract.record_cwd",
            capability_ref="shell.record_cwd",
            argv=["sh", "-c", f"pwd -P > {out}"],
            effect_predicate="working_directory_recorded",
            observer_ref="shell.pwd",
            observation_ref="contract:035-exec-cwd",
            gate="035-exec-cwd",
        )
        ledger = Ledger("memory")
        rc = m.admit_and_execute(action, ledger)

        assert rc == 0
        recorded = Path(out.read_text().strip()).resolve()
        assert recorded == Path(m.REPO_ROOT).resolve()

        # The real receipt state, not an interaction count.
        assert len(ledger.items) == 1
        assert ledger.items[0].verified is True
        assert ledger.items[0].standing == m.gymact.Standing.ALIVE
        assert ledger.items[0].reason == "exit_code=0"
