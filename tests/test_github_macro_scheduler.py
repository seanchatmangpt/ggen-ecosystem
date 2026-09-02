from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE_PATH = ROOT / "scripts" / "github_macro_governor.py"
SCHED_PATH = ROOT / "scripts" / "github_macro_scheduler.py"

core_spec = importlib.util.spec_from_file_location("github_macro_governor", CORE_PATH)
core = importlib.util.module_from_spec(core_spec)
assert core_spec and core_spec.loader
sys.modules[core_spec.name] = core
core_spec.loader.exec_module(core)

sched_spec = importlib.util.spec_from_file_location("github_macro_scheduler", SCHED_PATH)
sched = importlib.util.module_from_spec(sched_spec)
assert sched_spec and sched_spec.loader
sys.modules[sched_spec.name] = sched
sched_spec.loader.exec_module(sched)


def obs(n: int):
    return core.Observation(
        repo="seanchatmangpt/ggen-ecosystem",
        kind="workflow-abnormality",
        updated_at=f"2026-09-02T09:{59-n:02d}:00Z",
        identity=f"run:{n}",
        title=f"run {n}",
        url=f"https://example/{n}",
        action="manufacture-repair-demand",
        metadata={},
    )


POLICY = core.Policy(
    managed=(core.Repo("seanchatmangpt/ggen-ecosystem", "root", True, True),),
    capability_prefix="[capability]",
    authorized_issue_logins=("seanchatmangpt",),
    max_actions_per_run=3,
    max_observations_per_repo=50,
    observation_window_hours=72,
    agent_model="gpt-5.3-codex",
    agent_custom_agent="capability-manufacturer",
)


class MacroSchedulerTests(unittest.TestCase):
    def test_blocked_decisions_do_not_starve_later_actuation(self):
        def executor(item, policy, current_repo, apply):
            if item.identity in {"run:0", "run:1", "run:2"}:
                return {"standing": "BLOCKED[TOKEN_MISSING]", "applied": False}
            return {"standing": "ALIVE[ACTUATED]", "applied": True}

        got = sched.schedule_frontier(
            [obs(i) for i in range(6)], POLICY, "seanchatmangpt/ggen-ecosystem", True,
            max_actuations=1, max_decisions=6, executor=executor,
        )
        self.assertEqual(4, len(got))
        self.assertEqual(1, sum(bool(x.get("applied")) for x in got))
        self.assertEqual("run:3", got[-1]["source"]["identity"])

    def test_actuation_budget_is_hard_ceiling(self):
        def executor(item, policy, current_repo, apply):
            return {"standing": "ALIVE[ACTUATED]", "applied": True}

        got = sched.schedule_frontier(
            [obs(i) for i in range(10)], POLICY, "seanchatmangpt/ggen-ecosystem", True,
            max_actuations=3, max_decisions=10, executor=executor,
        )
        self.assertEqual(3, len(got))
        self.assertEqual(3, sum(bool(x.get("applied")) for x in got))

    def test_decision_budget_bounds_blocked_scan(self):
        def executor(item, policy, current_repo, apply):
            return {"standing": "BLOCKED[TOKEN_MISSING]", "applied": False}

        got = sched.schedule_frontier(
            [obs(i) for i in range(50)], POLICY, "seanchatmangpt/ggen-ecosystem", True,
            max_actuations=3, max_decisions=7, executor=executor,
        )
        self.assertEqual(7, len(got))
        self.assertEqual(0, sum(bool(x.get("applied")) for x in got))

    def test_apply_with_only_blocked_work_has_typed_blocked_standing(self):
        standing = sched.summary_standing(
            apply=True,
            candidates=[obs(0)],
            decisions=[{"standing": "BLOCKED[TOKEN_MISSING]", "applied": False}],
            errors=[],
        )
        self.assertEqual("BLOCKED[NO_ADMISSIBLE_ACTUATION_AUTHORITY]", standing)

    def test_plan_is_alive_without_actuation(self):
        standing = sched.summary_standing(
            apply=False, candidates=[obs(0)], decisions=[], errors=[]
        )
        self.assertEqual("ALIVE[PLAN]", standing)


if __name__ == "__main__":
    unittest.main()
