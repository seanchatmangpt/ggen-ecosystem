from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "github_macro_governor.py"
SPEC = importlib.util.spec_from_file_location("github_macro_governor", MODULE_PATH)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = mod
SPEC.loader.exec_module(mod)


class MacroGovernorTests(unittest.TestCase):
    def setUp(self):
        self.now = dt.datetime(2026, 9, 2, 9, 0, tzinfo=dt.timezone.utc)
        self.repo = mod.Repo(
            full_name="seanchatmangpt/ggen-ecosystem",
            role="root",
            write=True,
            agent=True,
        )

    def test_reverse_chronological_newest_first(self):
        older = mod.Observation(
            repo=self.repo.full_name,
            kind="capability-demand",
            updated_at="2026-09-02T08:00:00Z",
            identity="issue:1",
            title="[capability] old",
            url="https://example/1",
            action="delegate-agent",
            metadata={},
        )
        newer = mod.dataclasses.replace(
            older,
            updated_at="2026-09-02T08:30:00Z",
            identity="issue:2",
            title="[capability] new",
        )
        ordered = mod.reverse_chronological([older, newer])
        self.assertEqual(["issue:2", "issue:1"], [x.identity for x in ordered])

    def test_successful_workflows_are_not_unresolved(self):
        payload = {
            "workflow_runs": [
                {
                    "id": 1,
                    "name": "green",
                    "updated_at": "2026-09-02T08:30:00Z",
                    "status": "completed",
                    "conclusion": "success",
                    "html_url": "https://example/run/1",
                }
            ]
        }
        got = mod.normalize_workflow_runs(
            self.repo, payload, now=self.now, window_hours=72
        )
        self.assertEqual([], got)

    def test_timeout_gets_one_rerun_path(self):
        payload = {
            "workflow_runs": [
                {
                    "id": 2,
                    "name": "timeout",
                    "updated_at": "2026-09-02T08:30:00Z",
                    "status": "completed",
                    "conclusion": "timed_out",
                    "run_attempt": 1,
                    "html_url": "https://example/run/2",
                }
            ]
        }
        got = mod.normalize_workflow_runs(
            self.repo, payload, now=self.now, window_hours=72
        )
        self.assertEqual(1, len(got))
        self.assertEqual("rerun-failed", got[0].action)

    def test_deterministic_failure_manufactures_repair_demand(self):
        payload = {
            "workflow_runs": [
                {
                    "id": 3,
                    "name": "court",
                    "updated_at": "2026-09-02T08:30:00Z",
                    "status": "completed",
                    "conclusion": "failure",
                    "head_sha": "a" * 40,
                    "html_url": "https://example/run/3",
                }
            ]
        }
        got = mod.normalize_workflow_runs(
            self.repo, payload, now=self.now, window_hours=72
        )
        self.assertEqual("manufacture-repair-demand", got[0].action)
        body = mod.repair_body(got[0])
        self.assertIn("RCA", body)
        self.assertIn("macro-fingerprint:", body)

    def test_only_authorized_capability_issues_enter_pull_frontier(self):
        issues = [
            {
                "number": 1,
                "title": "[capability] untrusted",
                "updated_at": "2026-09-02T08:30:00Z",
                "html_url": "https://example/issues/1",
                "body": "",
                "labels": [],
                "user": {"login": "someone"},
            },
            {
                "number": 2,
                "title": "[capability] manufacture X",
                "updated_at": "2026-09-02T08:31:00Z",
                "html_url": "https://example/issues/2",
                "body": "Authority: implementation",
                "labels": [],
                "user": {"login": "seanchatmangpt"},
            },
        ]
        got = mod.normalize_issues(
            self.repo,
            issues,
            capability_prefix="[capability]",
            authorized_issue_logins=("seanchatmangpt", "github-actions[bot]"),
            now=self.now,
            window_hours=72,
        )
        self.assertEqual(2, len(got))
        by_id = {x.identity: x for x in got}
        self.assertEqual("observe", by_id["issue:1"].action)
        self.assertEqual("delegate-agent", by_id["issue:2"].action)

    def test_pull_requests_are_observation_only(self):
        pulls = [
            {
                "number": 4,
                "title": "candidate",
                "updated_at": "2026-09-02T08:31:00Z",
                "html_url": "https://example/pulls/4",
                "head": {"sha": "b" * 40},
                "base": {"ref": "main"},
                "draft": False,
            }
        ]
        got = mod.normalize_pulls(
            self.repo, pulls, now=self.now, window_hours=72
        )
        self.assertEqual("observe", got[0].action)
        self.assertFalse(mod.actionable(got[0]))

    def test_receipt_binds_policy_and_frontier(self):
        observation = mod.Observation(
            repo=self.repo.full_name,
            kind="workflow-abnormality",
            updated_at="2026-09-02T08:30:00Z",
            identity="run:9",
            title="court",
            url="https://example/run/9",
            action="manufacture-repair-demand",
            metadata={"head_sha": "c" * 40, "conclusion": "failure"},
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            policy = root / "governor.toml"
            policy.write_text("[governor]\nselection='newest'\n")
            receipt = root / "receipt.json"
            mod.write_receipt(
                receipt,
                policy,
                [observation],
                [],
                self.now,
                False,
                [],
            )
            doc = json.loads(receipt.read_text())
            self.assertEqual(1, doc["observation_count"])
            self.assertEqual("run:9", doc["frontier"][0]["identity"])
            self.assertTrue((root / "receipt.json.sha256").is_file())

    def test_missing_agent_token_is_typed_block_not_exception(self):
        observation = mod.Observation(
            repo=self.repo.full_name,
            kind="capability-demand",
            updated_at="2026-09-02T08:30:00Z",
            identity="issue:10",
            title="[capability] X",
            url="https://example/issues/10",
            action="delegate-agent",
            metadata={"issue_number": 10, "body": ""},
        )
        policy = mod.Policy(
            managed=(self.repo,),
            capability_prefix="[capability]",
            authorized_issue_logins=("seanchatmangpt", "github-actions[bot]"),
            max_actions_per_run=3,
            max_observations_per_repo=50,
            observation_window_hours=72,
            agent_model="gpt-5.3-codex",
            agent_custom_agent="capability-manufacturer",
        )
        old = os.environ.pop("COPILOT_AGENT_TOKEN", None)
        try:
            result = mod.delegate(observation, policy=policy, apply=True)
        finally:
            if old is not None:
                os.environ["COPILOT_AGENT_TOKEN"] = old
        self.assertEqual("BLOCKED[COPILOT_AGENT_TOKEN_MISSING]", result["standing"])



WORKFLOW_ID = 348179714  # Autonomic Crown workflow id observed on seanchatmangpt/ggen-ecosystem
REPO = "seanchatmangpt/ggen-ecosystem"


def _git(cwd: Path, *args: str) -> str:
    # hermetic_git_env scrubs inherited GIT_DIR & co.: without it git honours an ambient
    # GIT_DIR over -C and these fixture commits land in the caller's repository.
    env = mod.hermetic_git_env(
        GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
        GIT_COMMITTER_EMAIL="t@t", GIT_AUTHOR_DATE="2026-09-01T00:00:00Z",
        GIT_COMMITTER_DATE="2026-09-01T00:00:00Z")
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True,
                          text=True, env=env).stdout.strip()


def _run(run_id: int, head: str, conclusion: str, updated: str, *, workflow_id=WORKFLOW_ID,
         name="Autonomic Crown", status="completed") -> dict:
    return {"id": run_id, "name": name, "workflow_id": workflow_id, "head_sha": head,
            "status": status, "conclusion": conclusion, "updated_at": updated,
            "html_url": f"https://github.com/{REPO}/actions/runs/{run_id}", "run_attempt": 1}


class SubjectKeyedDemandTests(unittest.TestCase):
    """C17 / GGE-26922-14. Real collaborators: a real git object store is the ancestry oracle."""

    @classmethod
    def setUpClass(cls):
        cls._td = tempfile.TemporaryDirectory()
        root = Path(cls._td.name) / "repo"
        root.mkdir()
        _git(root, "init", "-q", "-b", "main")
        _git(root, "commit", "-q", "--allow-empty", "-m", "R")
        r = _git(root, "rev-parse", "HEAD")
        _git(root, "commit", "-q", "--allow-empty", "-m", "A")
        a = _git(root, "rev-parse", "HEAD")
        _git(root, "commit", "-q", "--allow-empty", "-m", "B")
        b = _git(root, "rev-parse", "HEAD")
        _git(root, "switch", "-q", "-c", "side", r)
        _git(root, "commit", "-q", "--allow-empty", "-m", "C")
        c = _git(root, "rev-parse", "HEAD")
        cls.root, cls.A, cls.B, cls.C = root, a, b, c
        cls.ancestry = mod.GitAncestry(root)

    @classmethod
    def tearDownClass(cls):
        cls._td.cleanup()

    def setUp(self):
        self.now = dt.datetime(2026, 9, 26, 9, 0, tzinfo=dt.timezone.utc)
        self.repo = mod.Repo(full_name=REPO, role="root", write=True, agent=True)

    def _failures(self, *runs):
        return mod.normalize_workflow_runs(self.repo, {"workflow_runs": list(runs)}, now=self.now,
                                           window_hours=72)

    def _demand_issue(self, number: int, item) -> dict:
        return {"number": number, "title": f"[capability][repair] {item.title}: failure",
                "body": mod.repair_body(item), "created_at": "2026-09-25T00:00:00Z"}

    # -- fingerprint is subject-keyed -------------------------------------------------------
    def test_three_failing_runs_same_subject_give_one_fingerprint(self):
        items = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"),
                               _run(2, self.A, "failure", "2026-09-25T02:00:00Z"),
                               _run(3, self.A, "failure", "2026-09-25T03:00:00Z"))
        self.assertEqual(3, len(items))
        self.assertEqual(3, len({x.identity for x in items}))
        self.assertEqual(1, len({mod.fingerprint(x) for x in items}))
        kept = mod.dedupe_demands(mod.reverse_chronological(items))
        self.assertEqual(["run:3"], [x.identity for x in kept])

    def test_distinct_subjects_keep_distinct_fingerprints(self):
        base = _run(1, self.A, "failure", "2026-09-25T01:00:00Z")
        variants = [base,
                    {**base, "id": 2, "head_sha": self.B},
                    {**base, "id": 3, "conclusion": "action_required"},
                    {**base, "id": 4, "workflow_id": 7, "name": "Other"}]
        items = self._failures(*variants)
        self.assertEqual(4, len({mod.fingerprint(x) for x in items}))
        other_repo = mod.dataclasses.replace(items[0], repo="seanchatmangpt/ggen")
        self.assertNotEqual(mod.fingerprint(items[0]), mod.fingerprint(other_repo))

    def test_dedupe_never_collapses_reruns(self):
        items = self._failures(_run(1, self.A, "timed_out", "2026-09-25T01:00:00Z"),
                               _run(2, self.A, "timed_out", "2026-09-25T02:00:00Z"))
        self.assertEqual(2, len(mod.dedupe_demands(items)))

    def test_existing_demand_matches_later_run_of_same_subject(self):
        first, later = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"),
                                      _run(9, self.A, "failure", "2026-09-25T09:00:00Z"))
        issues = [self._demand_issue(41, first)]
        self.assertEqual(41, mod.existing_demand(later, issues))
        other_head = self._failures(_run(10, self.B, "failure", "2026-09-25T10:00:00Z"))[0]
        self.assertIsNone(mod.existing_demand(other_head, issues))

    def test_existing_demand_matches_legacy_run_keyed_issue(self):
        legacy = {"number": 365, "title": "[capability][repair] Autonomic Crown: failure",
                  "created_at": "2026-09-23T00:32:35Z", "body": (
                      "Authority: implementation\n\n"
                      f"- source repository: `{REPO}`\n- source identity: `run:35801445133`\n"
                      f"- source URL: https://github.com/{REPO}/actions/runs/35801445133\n"
                      f"- head SHA: `{self.A}`\n- conclusion: `failure`\n\n"
                      "<!-- macro-fingerprint:2c1c8cbf7234a4998aaf62bc -->\n")}
        again = self._failures(_run(35824027486, self.A, "failure", "2026-09-25T08:00:00Z"))[0]
        self.assertEqual(365, mod.existing_demand(again, [legacy]))
        subject = mod.subject_of_issue(legacy, REPO)
        self.assertEqual(("Autonomic Crown", self.A, "failure", None),
                         (subject.workflow_name, subject.head_sha, subject.conclusion, subject.workflow_id))

    def test_subject_marker_round_trips(self):
        item = self._failures(_run(5, self.A, "failure", "2026-09-25T05:00:00Z"))[0]
        got = mod.subject_of_issue(self._demand_issue(7, item), REPO)
        self.assertEqual(mod.subject_of(item), got)
        self.assertIsNone(mod.subject_of_issue({"number": 8, "title": "[capability] x", "body": "no marker"}, REPO))
        self.assertIsNone(mod.subject_of_issue({"number": 9, "pull_request": {}, "body": mod.repair_body(item)}, REPO))

    # -- close-on-recovery ------------------------------------------------------------------
    def _reconcile(self, issues, *success_runs):
        recoveries = mod.normalize_recoveries(self.repo, {"workflow_runs": list(success_runs)})
        return mod.reconcile_demands(REPO, issues, recoveries, self.ancestry)

    def test_success_on_descendant_closes_with_recovery_run_id(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(36208447624, self.B, "success", "2026-09-26T01:26:49Z"))
        self.assertEqual("close-on-recovery", plan["action"])
        self.assertEqual("CLOSED[RECOVERY_RECEIPT]", plan["standing"])
        self.assertEqual(36208447624, plan["recovery_run_id"])
        self.assertEqual(self.B, plan["recovery_head_sha"])
        planned = mod.apply_recovery_close(plan, REPO, apply=False)
        self.assertEqual("PLANNED[CLOSED[RECOVERY_RECEIPT]]", planned["standing"])
        self.assertFalse(planned["applied"])

    def test_success_on_non_descendant_does_not_close(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(50, self.C, "success", "2026-09-26T01:00:00Z"))
        self.assertEqual("keep-open", plan["action"])
        self.assertEqual("OPEN[NO_RECOVERY_RECEIPT]", plan["standing"])
        self.assertNotIn("recovery_run_id", plan)

    def test_ancestor_head_success_does_not_close(self):
        demand = self._failures(_run(1, self.B, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(51, self.A, "success", "2026-09-26T01:00:00Z"))
        self.assertEqual("keep-open", plan["action"])

    def test_success_of_different_workflow_does_not_close(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(52, self.B, "success", "2026-09-26T01:00:00Z",
                                       workflow_id=7, name="Autonomic Crown"))
        self.assertEqual("keep-open", plan["action"])

    def test_success_older_than_demand_does_not_close(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(53, self.B, "success", "2026-09-25T00:59:59Z"))
        self.assertEqual("keep-open", plan["action"])

    def test_unknown_head_is_typed_ancestry_unknown(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(54, "f" * 40, "success", "2026-09-26T01:00:00Z"))
        self.assertEqual("OPEN[ANCESTRY_UNKNOWN]", plan["standing"])

    def test_non_success_runs_are_not_recovery_evidence(self):
        runs = [_run(60, self.B, "failure", "2026-09-26T01:00:00Z"),
                _run(61, self.B, "", "2026-09-26T01:00:00Z", status="in_progress"),
                _run(62, self.B, "skipped", "2026-09-26T01:00:00Z")]
        self.assertEqual([], mod.normalize_recoveries(self.repo, {"workflow_runs": runs}))

    def test_legacy_duplicates_close_and_other_demands_stay_open(self):
        def legacy(number, run_id, head, created):
            return {"number": number, "title": "[capability][repair] Autonomic Crown: failure",
                    "created_at": created, "body": (
                        f"- source repository: `{REPO}`\n- source identity: `run:{run_id}`\n"
                        f"- head SHA: `{head}`\n- conclusion: `failure`\n\n<!-- macro-fingerprint:x -->\n")}
        other = self._failures(_run(70, self.A, "failure", "2026-09-25T01:00:00Z",
                                    workflow_id=7, name="Court"))[0]
        issues = [legacy(365, 35801445133, self.A, "2026-09-23T00:32:35Z"),
                  legacy(366, 35824027486, self.A, "2026-09-23T08:27:10Z"),
                  legacy(368, 1, self.C, "2026-09-23T09:00:00Z"),
                  self._demand_issue(400, other),
                  {"number": 401, "title": "[capability] manual", "body": "hand written"}]
        plans = self._reconcile(issues, _run(36208447624, self.B, "success", "2026-09-26T01:26:49Z"))
        by_issue = {p["issue_number"]: p for p in plans}
        self.assertEqual({365, 366, 368, 400}, set(by_issue))
        self.assertEqual("close-on-recovery", by_issue[365]["action"])
        self.assertEqual("close-on-recovery", by_issue[366]["action"])
        self.assertEqual(36208447624, by_issue[366]["recovery_run_id"])
        self.assertEqual("keep-open", by_issue[368]["action"])  # success head B does not descend from demand head C
        self.assertEqual("keep-open", by_issue[400]["action"])  # different workflow

    def test_close_without_recovery_run_id_is_refused(self):
        forged = {"action": "close-on-recovery", "target": REPO, "issue_number": 1, "applied": False,
                  "standing": "CLOSED[RECOVERY_RECEIPT]", "subject": {}}
        saved = {k: os.environ.pop(k, None) for k in ("GITHUB_TOKEN", "MACRO_GITHUB_TOKEN")}
        try:  # no credential reachable: a regression can never write to a real issue
            got = mod.apply_recovery_close(forged, REPO, apply=True)
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v
        self.assertEqual("REFUSED[NO_RECOVERY_RUN_ID]", got["standing"])
        self.assertFalse(got["applied"])

    def test_apply_close_without_token_is_typed_block(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        (plan,) = self._reconcile([self._demand_issue(41, demand)],
                                  _run(80, self.B, "success", "2026-09-26T01:00:00Z"))
        saved = {k: os.environ.pop(k, None) for k in ("GITHUB_TOKEN", "MACRO_GITHUB_TOKEN")}
        try:
            got = mod.apply_recovery_close(plan, REPO, apply=True)
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v
        self.assertEqual("BLOCKED[GITHUB_TOKEN_MISSING]", got["standing"])

    def test_recovery_comment_cites_run_id(self):
        subject = mod.DemandSubject(REPO, WORKFLOW_ID, "Autonomic Crown", self.A, "failure")
        rec = mod.Recovery(REPO, 36208447624, WORKFLOW_ID, "Autonomic Crown", self.B,
                           "2026-09-26T01:26:49Z", "https://example/run/36208447624")
        body = mod.recovery_comment(subject, rec)
        self.assertIn("recovery run id: `36208447624`", body)
        self.assertIn("<!-- macro-recovery:36208447624 -->", body)
        self.assertIn("CLOSED[RECOVERY_RECEIPT]", body)

    def test_receipt_records_recovery_decision(self):
        demand = self._failures(_run(1, self.A, "failure", "2026-09-25T01:00:00Z"))[0]
        plans = self._reconcile([self._demand_issue(41, demand)],
                                _run(90, self.B, "success", "2026-09-26T01:00:00Z"))
        with tempfile.TemporaryDirectory() as td:
            policy, receipt = Path(td) / "governor.toml", Path(td) / "receipt.json"
            policy.write_text("[governor]\n")
            mod.write_receipt(receipt, policy, [demand], plans, self.now, False, [])
            doc = json.loads(receipt.read_text())
        self.assertEqual(90, doc["decisions"][0]["recovery_run_id"])
        self.assertEqual("CLOSED[RECOVERY_RECEIPT]", doc["decisions"][0]["standing"])


def _repo_state(repo: Path) -> str:
    """Refs, HEAD, reflog and object counts: any commit or ref move in ``repo`` changes it."""
    return "\n".join([
        _git(repo, "for-each-ref"),
        _git(repo, "symbolic-ref", "HEAD"),
        _git(repo, "reflog", "--all"),
        _git(repo, "count-objects", "-v"),
    ])


class GitEnvHermeticityTests(unittest.TestCase):
    """GGE v26.9.26 gge-governor-test-git-env-hermeticity. Real git, real subprocesses."""

    def test_scrub_list_covers_every_git_local_env_var(self):
        # Git itself is the oracle for which variables relocate the repository.
        local = subprocess.run(["git", "rev-parse", "--local-env-vars"], check=True,
                               capture_output=True, text=True).stdout.split()
        self.assertTrue(local)
        self.assertEqual([], sorted(set(local) - set(mod.GIT_LOCAL_ENV_VARS)))

    def test_hermetic_env_drops_location_vars_and_keeps_everything_else(self):
        base = {v: "/elsewhere" for v in mod.GIT_LOCAL_ENV_VARS}
        base.update({"PATH": "/bin", "HOME": "/h", "GIT_AUTHOR_NAME": "x", "GIT_DIRX": "keep"})
        env = mod.hermetic_git_env(base, GIT_AUTHOR_NAME="t")
        self.assertEqual({"PATH": "/bin", "HOME": "/h", "GIT_AUTHOR_NAME": "t", "GIT_DIRX": "keep"}, env)
        self.assertIn("GIT_DIR", base)  # the caller's mapping is not mutated

    def test_hermetic_env_empty_base_and_default_is_os_environ(self):
        self.assertEqual({}, mod.hermetic_git_env({}))
        self.assertEqual({"A": "1"}, mod.hermetic_git_env({}, A="1"))
        default = mod.hermetic_git_env()
        self.assertEqual({k: v for k, v in os.environ.items() if k not in mod.GIT_LOCAL_ENV_VARS},
                         default)

    def _sentinel(self, td: str) -> Path:
        sentinel = Path(td) / "sentinel"
        sentinel.mkdir()
        _git(sentinel, "init", "-q", "-b", "main")
        _git(sentinel, "commit", "-q", "--allow-empty", "-m", "sentinel")
        return sentinel

    def test_ancestry_ignores_ambient_git_dir(self):
        # A real child process with GIT_DIR pointing at an unrelated repo must still answer
        # ancestry from the git_dir it was constructed with.
        with tempfile.TemporaryDirectory() as td:
            sentinel = self._sentinel(td)
            repo = Path(td) / "repo"
            repo.mkdir()
            _git(repo, "init", "-q", "-b", "main")
            _git(repo, "commit", "-q", "--allow-empty", "-m", "R")
            r = _git(repo, "rev-parse", "HEAD")
            _git(repo, "commit", "-q", "--allow-empty", "-m", "A")
            a = _git(repo, "rev-parse", "HEAD")
            code = ("import importlib.util, sys; from pathlib import Path\n"
                    f"s = importlib.util.spec_from_file_location('g', {str(MODULE_PATH)!r})\n"
                    "m = importlib.util.module_from_spec(s); sys.modules['g'] = m; s.loader.exec_module(m)\n"
                    f"g = m.GitAncestry(Path({str(repo)!r}))\n"
                    f"print(g('x', {r!r}, {a!r}), g('x', {a!r}, {r!r}), g('x', 'f' * 40, {a!r}))\n")
            env = {**os.environ, "GIT_DIR": str(sentinel / ".git")}
            out = subprocess.run([sys.executable, "-c", code], env=env, check=True,
                                 capture_output=True, text=True).stdout.split()
        self.assertEqual(["True", "False", "None"], out)

    def test_suite_under_ambient_git_dir_leaves_sentinel_repo_byte_identical(self):
        with tempfile.TemporaryDirectory() as td:
            sentinel = self._sentinel(td)
            before = _repo_state(sentinel)
            env = {**os.environ, "GIT_DIR": str(sentinel / ".git")}
            env.pop("GIT_WORK_TREE", None)
            proc = subprocess.run(
                [sys.executable, "-m", "unittest", "tests.test_github_macro_governor.SubjectKeyedDemandTests"],
                cwd=MODULE_PATH.parents[1], env=env, capture_output=True, text=True)
            after = _repo_state(sentinel)
        self.assertEqual(0, proc.returncode, proc.stderr[-2000:])
        self.assertRegex(proc.stderr, r"Ran [1-9]\d* tests")
        self.assertEqual(before, after)
        self.assertNotIn("refs/heads/side", after)


if __name__ == "__main__":
    unittest.main()
