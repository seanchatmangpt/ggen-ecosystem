from __future__ import annotations

import datetime as dt
import importlib.util
import json
import os
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


if __name__ == "__main__":
    unittest.main()
