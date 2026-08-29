from types import SimpleNamespace
from support import Ledger, load_module

def test_execution_is_repo_confined(monkeypatch):
    m, seen = load_module(), {}
    monkeypatch.setattr(m.subprocess, "run", lambda argv, **kw: (seen.update(kw), SimpleNamespace(returncode=0, stderr=""))[1])
    m.admit_and_execute(m.SAFE_ACTIONS[0], Ledger("memory"))
    assert seen["cwd"] == m.REPO_ROOT
