#!/usr/bin/env python3
"""DfCM SELECT plane for the GitHub macro governor.

Blocked authority and idempotent NOOP decisions are evidence, not actuations and
therefore never consume the bounded actuation budget.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import os
import tomllib
from pathlib import Path
from typing import Any, Callable

import github_macro_governor as core

Executor = Callable[[core.Observation, core.Policy, str, bool], dict[str, Any]]


def scheduler_limits(policy_path: Path, policy: core.Policy) -> tuple[int, int]:
    doc = tomllib.loads(policy_path.read_text())
    g = doc["governor"]
    max_actuations = int(g.get("max_actuations_per_run", g.get("max_actions_per_run", 3)))
    max_decisions = int(g.get("max_decisions_per_run", max(max_actuations, 25)))
    if max_actuations < 0 or max_decisions < 0:
        raise ValueError("REFUSED[NEGATIVE_MACRO_BUDGET]")
    if max_decisions < max_actuations:
        raise ValueError("REFUSED[DECISION_BUDGET_LT_ACTUATION_BUDGET]")
    return max_actuations, max_decisions


def schedule_frontier(
    candidates: list[core.Observation],
    policy: core.Policy,
    current_repo: str,
    apply: bool,
    *,
    max_actuations: int,
    max_decisions: int,
    executor: Executor = core.execute,
) -> list[dict[str, Any]]:
    """Walk newest→oldest until decision or actual actuation budget is exhausted."""
    decisions: list[dict[str, Any]] = []
    actuations = 0
    for item in candidates:
        if len(decisions) >= max_decisions or actuations >= max_actuations:
            break
        try:
            decision = executor(item, policy, current_repo, apply)
        except Exception as exc:
            decision = {
                "action": item.action,
                "target": item.repo,
                "applied": False,
                "standing": "BUILD_BROKEN[MACRO_ACTION_EXCEPTION]",
                "error": str(exc),
            }
        decision["source"] = {
            "kind": item.kind,
            "identity": item.identity,
            "updated_at": item.updated_at,
            "url": item.url,
        }
        decisions.append(decision)
        if bool(decision.get("applied")):
            actuations += 1
    return decisions


def summary_standing(
    *, apply: bool, candidates: list[core.Observation], decisions: list[dict[str, Any]], errors: list[dict[str, str]]
) -> str:
    if errors:
        return "PARTIAL_ALIVE[COLLECTION_ERRORS]"
    if any(str(d.get("standing", "")).startswith("BUILD_BROKEN") for d in decisions):
        return "BUILD_BROKEN[MACRO_ACTION_EXCEPTION]"
    if not apply:
        return "ALIVE[PLAN]"
    acted = sum(bool(d.get("applied")) for d in decisions)
    if acted:
        return "ALIVE[ACTUATED]"
    if candidates:
        return "BLOCKED[NO_ADMISSIBLE_ACTUATION_AUTHORITY]"
    return "ALIVE[NO_UNRESOLVED_ACTIONABLE_WORK]"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", type=Path, default=Path("macro/governor.toml"))
    ap.add_argument("--receipt", type=Path, default=Path("macro/receipt.json"))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--repo", action="append", default=[])
    args = ap.parse_args(argv)

    started = core.now()
    policy = core.load_policy(args.policy)
    max_actuations, max_decisions = scheduler_limits(args.policy, policy)
    # Preserve compatibility with the v1 execution adapter while making the new
    # field name semantically explicit at SELECT.
    policy = dataclasses.replace(policy, max_actions_per_run=max_actuations)

    if args.repo:
        scope = set(args.repo)
        policy = dataclasses.replace(
            policy, managed=tuple(r for r in policy.managed if r.full_name in scope)
        )
        if not policy.managed:
            raise SystemExit("REFUSED[NO_CONFIGURED_REPOSITORY_SELECTED]")

    current_repo = os.environ.get("GITHUB_REPOSITORY", "seanchatmangpt/ggen-ecosystem")
    api = core.GitHub(os.environ.get("MACRO_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN"))
    observations: list[core.Observation] = []
    errors: list[dict[str, str]] = []
    current = core.now()
    for repo in policy.managed:
        try:
            observations.extend(core.collect(api, repo, policy, current))
        except Exception as exc:
            errors.append({"repo": repo.full_name, "error": str(exc)})

    observations = core.reverse_chronological(observations)
    candidates = [x for x in observations if core.actionable(x)]
    decisions = schedule_frontier(
        candidates,
        policy,
        current_repo,
        args.apply,
        max_actuations=max_actuations,
        max_decisions=max_decisions,
    )

    core.write_receipt(args.receipt, args.policy, observations, decisions, started, args.apply, errors)
    acted = sum(bool(d.get("applied")) for d in decisions)
    standing = summary_standing(
        apply=args.apply, candidates=candidates, decisions=decisions, errors=errors
    )
    summary = {
        "standing": standing,
        "mode": "apply" if args.apply else "plan",
        "observations": len(observations),
        "actionable": len(candidates),
        "decisions": len(decisions),
        "acted": acted,
        "blocked": sum(str(d.get("standing", "")).startswith("BLOCKED") for d in decisions),
        "noop": sum(str(d.get("standing", "")).startswith("NOOP") for d in decisions),
        "max_actuations": max_actuations,
        "max_decisions": max_decisions,
        "collection_errors": len(errors),
        "receipt": str(args.receipt),
    }
    print(json.dumps(summary, sort_keys=True))
    return 2 if standing.startswith("BUILD_BROKEN") else 0


if __name__ == "__main__":
    raise SystemExit(main())
