#!/usr/bin/env python3
"""Cross-repository GitHub macro governor: newest unresolved evidence first."""
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

API = "https://api.github.com"
VERSION = "2026-03-10"


@dataclasses.dataclass(frozen=True)
class Repo:
    full_name: str
    role: str
    write: bool
    agent: bool


@dataclasses.dataclass(frozen=True)
class Policy:
    managed: tuple[Repo, ...]
    capability_prefix: str
    authorized_issue_logins: tuple[str, ...]
    max_actions_per_run: int
    max_observations_per_repo: int
    observation_window_hours: int
    agent_model: str
    agent_custom_agent: str


@dataclasses.dataclass(frozen=True)
class Observation:
    repo: str
    kind: str
    updated_at: str
    identity: str
    title: str
    url: str
    action: str
    metadata: dict[str, Any]

    @property
    def timestamp(self) -> dt.datetime:
        return parse_time(self.updated_at)


class GitHub:
    def __init__(self, token: str | None):
        self.token = token

    def request(self, method: str, path: str, body: dict[str, Any] | None = None) -> Any:
        data = None if body is None else json.dumps(body, separators=(",", ":")).encode()
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "ggen-macro-governor/1",
            "X-GitHub-Api-Version": VERSION,
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(
            path if path.startswith("http") else API + path,
            data=data,
            method=method,
            headers=headers,
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                raw = res.read()
                return None if not raw else json.loads(raw)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode(errors="replace")
            raise RuntimeError(f"GitHub {method} {path}: HTTP {exc.code}: {body[:600]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"GitHub {method} {path}: {exc}") from exc

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        return self.request("POST", path, body)

    def patch(self, path: str, body: dict[str, Any]) -> Any:
        return self.request("PATCH", path, body)


def parse_time(value: str) -> dt.datetime:
    value = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = dt.datetime.fromisoformat(value)
    return (parsed if parsed.tzinfo else parsed.replace(tzinfo=dt.timezone.utc)).astimezone(dt.timezone.utc)


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def load_policy(path: Path) -> Policy:
    doc = tomllib.loads(path.read_text())
    g = doc["governor"]
    repos = tuple(
        Repo(str(x["name"]), str(x.get("role", "managed")), bool(x.get("write")), bool(x.get("agent")))
        for x in doc.get("repository", [])
    )
    if not repos:
        raise ValueError("REFUSED[NO_MANAGED_REPOSITORIES]")
    return Policy(
        repos,
        str(g.get("capability_prefix", "[capability]")),
        tuple(str(x) for x in g.get("authorized_issue_logins", ["seanchatmangpt", "github-actions[bot]"])),
        int(g.get("max_actions_per_run", 3)),
        int(g.get("max_observations_per_repo", 50)),
        int(g.get("observation_window_hours", 72)),
        str(g.get("agent_model", "gpt-5.3-codex")),
        str(g.get("custom_agent", "capability-manufacturer")),
    )


def in_window(value: str, current: dt.datetime, hours: int) -> bool:
    return parse_time(value) >= current - dt.timedelta(hours=hours)


def normalize_workflow_runs(repo: Repo, payload: dict[str, Any], *, now: dt.datetime, window_hours: int) -> list[Observation]:
    out = []
    for run in payload.get("workflow_runs", []):
        updated = str(run.get("updated_at") or run.get("created_at") or "")
        if not updated or not in_window(updated, now, window_hours):
            continue
        status, conclusion = str(run.get("status") or ""), str(run.get("conclusion") or "")
        meta = {
            "run_id": run["id"], "status": status, "conclusion": conclusion,
            "head_sha": run.get("head_sha"), "event": run.get("event"),
            "run_attempt": run.get("run_attempt", 1), "workflow_id": run.get("workflow_id"),
            "workflow_name": run.get("name"),
        }
        if status != "completed":
            action, kind = "observe", "workflow-active"
        elif conclusion in {"success", "skipped", "neutral"}:
            continue
        elif conclusion == "timed_out":
            action, kind = "rerun-failed", "workflow-abnormality"
        elif conclusion in {"cancelled", "stale"}:
            action, kind = "observe", "workflow-abnormality"
        else:
            action, kind = "manufacture-repair-demand", "workflow-abnormality"
        out.append(Observation(repo.full_name, kind, updated, f"run:{run['id']}",
                               str(run.get("name") or run.get("display_title") or "workflow"),
                               str(run.get("html_url") or ""), action, meta))
    return out


def normalize_issues(repo: Repo, payload: list[dict[str, Any]], *, capability_prefix: str,
                     authorized_issue_logins: tuple[str, ...], now: dt.datetime,
                     window_hours: int) -> list[Observation]:
    out, allowed = [], set(authorized_issue_logins)
    for issue in payload:
        title = str(issue.get("title") or "")
        if "pull_request" in issue or not title.casefold().startswith(capability_prefix.casefold()):
            continue
        updated = str(issue.get("updated_at") or issue.get("created_at") or "")
        if not updated or not in_window(updated, now, window_hours):
            continue
        author = str((issue.get("user") or {}).get("login") or "")
        admitted = author in allowed
        out.append(Observation(
            repo.full_name,
            "capability-demand" if admitted else "capability-demand-unadmitted",
            updated, f"issue:{issue['number']}", title, str(issue.get("html_url") or ""),
            "delegate-agent" if repo.agent and admitted else "observe",
            {"issue_number": issue["number"], "body": issue.get("body") or "", "author": author, "admitted": admitted},
        ))
    return out


def normalize_pulls(repo: Repo, payload: list[dict[str, Any]], *, now: dt.datetime,
                    window_hours: int) -> list[Observation]:
    out = []
    for pr in payload:
        updated = str(pr.get("updated_at") or pr.get("created_at") or "")
        if not updated or not in_window(updated, now, window_hours):
            continue
        out.append(Observation(
            repo.full_name, "open-pr", updated, f"pr:{pr['number']}",
            str(pr.get("title") or ""), str(pr.get("html_url") or ""), "observe",
            {"pr_number": pr["number"], "head_sha": (pr.get("head") or {}).get("sha"),
             "base_ref": (pr.get("base") or {}).get("ref"), "draft": pr.get("draft")},
        ))
    return out


def collect(api: GitHub, repo: Repo, policy: Policy, current: dt.datetime) -> list[Observation]:
    q = urllib.parse.quote(repo.full_name, safe="/")
    n = max(1, min(policy.max_observations_per_repo, 100))
    runs = api.get(f"/repos/{q}/actions/runs?per_page={n}")
    issues = api.get(f"/repos/{q}/issues?state=open&sort=updated&direction=desc&per_page={n}")
    pulls = api.get(f"/repos/{q}/pulls?state=open&sort=updated&direction=desc&per_page={n}")
    return (
        normalize_workflow_runs(repo, runs, now=current, window_hours=policy.observation_window_hours)
        + normalize_issues(repo, issues, capability_prefix=policy.capability_prefix,
                           authorized_issue_logins=policy.authorized_issue_logins,
                           now=current, window_hours=policy.observation_window_hours)
        + normalize_pulls(repo, pulls, now=current, window_hours=policy.observation_window_hours)
    )


def collect_reconciliations(api: GitHub, repo: Repo, policy: Policy, ancestry: Ancestry) -> list[dict[str, Any]]:
    q = urllib.parse.quote(repo.full_name, safe="/")
    n = max(1, min(policy.max_observations_per_repo, 100))
    successes = api.get(f"/repos/{q}/actions/runs?status=success&per_page={n}")
    issues = api.get(f"/repos/{q}/issues?state=open&per_page=100")
    return reconcile_demands(repo.full_name, issues, normalize_recoveries(repo, successes), ancestry)


def reverse_chronological(items: list[Observation]) -> list[Observation]:
    return sorted(items, key=lambda x: (x.timestamp, x.repo, x.identity), reverse=True)


def actionable(item: Observation) -> bool:
    return item.action not in {"observe", "none"}


# --- Subject-keyed demand (C17 / GGE-26922-14) -------------------------------------------
#
# A repair demand is keyed by its SUBJECT (repo, workflow, head_sha, conclusion), never by the
# run that observed it: N failing runs of one workflow on one head with one failure class are
# one defect and therefore one demand.  A demand closes only on a RECOVERY RECEIPT: a later
# success run of the same workflow on a head that descends from (or equals) the demand head.
# Every other open demand stays open (anti-windup: the demand count cannot be zeroed by closing).

SUBJECT_SCHEMA = "macro-demand-subject/v2"
SUBJECT_MARKER = re.compile(r"<!-- macro-subject:(\{.*\}) -->")
LEGACY_TITLE = re.compile(r"^\[capability\]\[repair\] (?P<name>.+): (?P<conclusion>[^:]+)$")
LEGACY_FIELD = re.compile(r"^- (?P<key>source repository|head SHA|conclusion): `(?P<value>[^`]*)`$", re.M)


@dataclasses.dataclass(frozen=True)
class DemandSubject:
    repo: str
    workflow_id: int | None
    workflow_name: str
    head_sha: str
    conclusion: str
    observed_at: str = ""

    def workflow_key(self) -> str:
        return f"id:{self.workflow_id}" if self.workflow_id is not None else f"name:{self.workflow_name}"

    def key(self) -> dict[str, str]:
        return {"schema": SUBJECT_SCHEMA, "repo": self.repo, "workflow": self.workflow_key(),
                "head_sha": self.head_sha, "conclusion": self.conclusion}

    def same_workflow(self, workflow_id: int | None, workflow_name: str) -> bool:
        if self.workflow_id is not None and workflow_id is not None:
            return self.workflow_id == workflow_id
        return bool(self.workflow_name) and self.workflow_name == workflow_name

    def same_subject(self, other: "DemandSubject") -> bool:
        return (self.repo == other.repo and self.head_sha == other.head_sha
                and self.conclusion == other.conclusion
                and self.same_workflow(other.workflow_id, other.workflow_name))


def _workflow_id(value: Any) -> int | None:
    try:
        return None if value is None or value == "" else int(value)
    except (TypeError, ValueError):
        return None


def subject_of(item: Observation) -> DemandSubject:
    meta = item.metadata
    return DemandSubject(
        repo=item.repo,
        workflow_id=_workflow_id(meta.get("workflow_id")),
        workflow_name=str(meta.get("workflow_name") or item.title or ""),
        head_sha=str(meta.get("head_sha") or "UNKNOWN"),
        conclusion=str(meta.get("conclusion") or "UNKNOWN"),
        observed_at=item.updated_at,
    )


def fingerprint(item: Observation) -> str:
    """Subject key (repo, workflow, head_sha, conclusion). The run id is deliberately absent."""
    doc = subject_of(item).key()
    return hashlib.sha256(json.dumps(doc, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:24]


def subject_of_issue(issue: dict[str, Any], repo: str) -> DemandSubject | None:
    """Recover the demand subject from an open repair issue; None if it is not a governor demand.

    v2 bodies carry an explicit ``macro-subject`` marker.  Legacy (run-keyed) bodies are parsed
    from their field lines and title so pre-existing duplicates (e.g. #365/#366) are reconcilable.
    """
    body = str(issue.get("body") or "")
    if "pull_request" in issue or "<!-- macro-fingerprint:" not in body:
        return None
    m = SUBJECT_MARKER.search(body)
    if m:
        try:
            doc = json.loads(m.group(1))
            return DemandSubject(str(doc["repo"]), _workflow_id(doc.get("workflow_id")),
                                 str(doc.get("workflow_name") or ""), str(doc["head_sha"]),
                                 str(doc["conclusion"]), str(doc.get("observed_at") or ""))
        except (KeyError, ValueError, TypeError):
            return None
    fields = {x.group("key"): x.group("value") for x in LEGACY_FIELD.finditer(body)}
    title = LEGACY_TITLE.match(str(issue.get("title") or ""))
    head = fields.get("head SHA", "")
    if not title or not head or head == "UNKNOWN":
        return None
    return DemandSubject(fields.get("source repository") or repo, None, title.group("name"), head,
                         fields.get("conclusion") or title.group("conclusion"),
                         str(issue.get("created_at") or ""))


@dataclasses.dataclass(frozen=True)
class Recovery:
    repo: str
    run_id: int
    workflow_id: int | None
    workflow_name: str
    head_sha: str
    updated_at: str
    url: str


def normalize_recoveries(repo: Repo, payload: dict[str, Any]) -> list[Recovery]:
    """Completed success runs: the only admissible evidence for closing a demand."""
    out = []
    for run in payload.get("workflow_runs", []):
        if str(run.get("status") or "") != "completed" or str(run.get("conclusion") or "") != "success":
            continue
        head, updated = run.get("head_sha"), str(run.get("updated_at") or run.get("created_at") or "")
        if not head or not updated:
            continue
        out.append(Recovery(repo.full_name, int(run["id"]), _workflow_id(run.get("workflow_id")),
                            str(run.get("name") or ""), str(head), updated, str(run.get("html_url") or "")))
    return out


# Ancestry oracle: (repo, ancestor_sha, descendant_sha) -> True | False | None (unknown).
Ancestry = Callable[[str, str, str], "bool | None"]


# Repository-location variables git honours over ``-C <path>`` (the set printed by
# ``git rev-parse --local-env-vars``, the same list git's own submodule machinery clears).
# An inherited GIT_DIR (Mode P / scratch-archive lanes export one) would otherwise redirect
# every git call here -- reads *and* writes -- into the caller's repository.
GIT_LOCAL_ENV_VARS = (
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_CONFIG", "GIT_CONFIG_PARAMETERS", "GIT_CONFIG_COUNT",
    "GIT_OBJECT_DIRECTORY", "GIT_DIR", "GIT_WORK_TREE", "GIT_IMPLICIT_WORK_TREE", "GIT_GRAFT_FILE",
    "GIT_INDEX_FILE", "GIT_NO_REPLACE_OBJECTS", "GIT_REPLACE_REF_BASE", "GIT_PREFIX",
    "GIT_SHALLOW_FILE", "GIT_COMMON_DIR",
)


def hermetic_git_env(base: "dict[str, str] | None" = None, **overrides: str) -> dict[str, str]:
    """``base`` (default ``os.environ``) minus GIT_LOCAL_ENV_VARS, plus ``overrides``.

    Git then resolves the repository from ``-C <path>`` alone, so an ambient GIT_DIR can
    never make a call read from or write to another repository.
    """
    env = {k: v for k, v in (os.environ if base is None else base).items()
           if k not in GIT_LOCAL_ENV_VARS}
    env.update(overrides)
    return env


class GitAncestry:
    """Ancestry from a local git object store (``git merge-base --is-ancestor``).

    Runs under ``hermetic_git_env()``: the answer comes from ``git_dir``, never from an
    inherited GIT_DIR/GIT_OBJECT_DIRECTORY.
    """

    def __init__(self, git_dir: Path):
        self.git_dir = git_dir

    def __call__(self, repo: str, ancestor: str, descendant: str) -> bool | None:
        res = subprocess.run(["git", "-C", str(self.git_dir), "merge-base", "--is-ancestor", ancestor, descendant],
                             capture_output=True, text=True, env=hermetic_git_env())
        return {0: True, 1: False}.get(res.returncode)


class GitHubAncestry:
    """Ancestry from the GitHub compare API: base...head status ahead|identical => base is an ancestor."""

    def __init__(self, api: GitHub):
        self.api = api

    def __call__(self, repo: str, ancestor: str, descendant: str) -> bool | None:
        q = urllib.parse.quote(repo, safe="/")
        try:
            doc = self.api.get(f"/repos/{q}/compare/{ancestor}...{descendant}")
        except RuntimeError:
            return None
        status = str((doc or {}).get("status") or "")
        if status in {"ahead", "identical"}:
            return True
        if status in {"behind", "diverged"}:
            return False
        return None


def find_recovery(subject: DemandSubject, recoveries: list[Recovery], ancestry: Ancestry,
                  not_before: str = "") -> tuple[Recovery | None, str]:
    """Newest admissible recovery for ``subject`` and a typed reason when there is none."""
    floor = parse_time(not_before or subject.observed_at) if (not_before or subject.observed_at) else None
    unknown = False
    for rec in sorted(recoveries, key=lambda r: (parse_time(r.updated_at), r.run_id), reverse=True):
        if rec.repo != subject.repo or not subject.same_workflow(rec.workflow_id, rec.workflow_name):
            continue
        if floor is not None and parse_time(rec.updated_at) <= floor:
            continue
        verdict = ancestry(subject.repo, subject.head_sha, rec.head_sha)
        if verdict is True:
            return rec, "CLOSED[RECOVERY_RECEIPT]"
        if verdict is None:
            unknown = True
    return None, "OPEN[ANCESTRY_UNKNOWN]" if unknown else "OPEN[NO_RECOVERY_RECEIPT]"


def recovery_comment(subject: DemandSubject, rec: Recovery) -> str:
    return f"""Macro governor recovery receipt: CLOSED[RECOVERY_RECEIPT]

- demand subject: `{subject.repo}` workflow `{subject.workflow_name or subject.workflow_key()}` head `{subject.head_sha}` conclusion `{subject.conclusion}`
- recovery run id: `{rec.run_id}`
- recovery run URL: {rec.url}
- recovery head SHA: `{rec.head_sha}` (descends from demand head)
- recovery observed at: `{rec.updated_at}`

<!-- macro-recovery:{rec.run_id} -->
"""


def reconcile_demands(repo: str, issues: list[dict[str, Any]], recoveries: list[Recovery],
                      ancestry: Ancestry) -> list[dict[str, Any]]:
    """Plan close-on-recovery for every open governor demand in ``repo``; others stay open."""
    plans = []
    for issue in issues:
        subject = subject_of_issue(issue, repo)
        if subject is None:
            continue
        rec, standing = find_recovery(subject, recoveries, ancestry,
                                      not_before=subject.observed_at or str(issue.get("created_at") or ""))
        plan = {"action": "close-on-recovery" if rec else "keep-open", "target": repo,
                "issue_number": issue.get("number"), "subject": dataclasses.asdict(subject),
                "applied": False, "standing": standing}
        if rec:
            plan["recovery_run_id"] = rec.run_id
            plan["recovery_url"] = rec.url
            plan["recovery_head_sha"] = rec.head_sha
        plans.append(plan)
    return plans


def apply_recovery_close(plan: dict[str, Any], current_repo: str, apply: bool) -> dict[str, Any]:
    if plan["action"] != "close-on-recovery":
        return plan
    if "recovery_run_id" not in plan:
        return {**plan, "standing": "REFUSED[NO_RECOVERY_RUN_ID]"}
    if not apply:
        return {**plan, "standing": "PLANNED[CLOSED[RECOVERY_RECEIPT]]"}
    token, name = token_for(plan["target"], current_repo)
    if not token:
        return {**plan, "standing": f"BLOCKED[{name}_MISSING]"}
    api, q = GitHub(token), urllib.parse.quote(plan["target"], safe="/")
    s = plan["subject"]
    subject = DemandSubject(s["repo"], s["workflow_id"], s["workflow_name"], s["head_sha"], s["conclusion"],
                            s.get("observed_at", ""))
    rec = Recovery(plan["target"], int(plan["recovery_run_id"]), None, s["workflow_name"],
                   plan["recovery_head_sha"], "", plan.get("recovery_url", ""))
    api.post(f"/repos/{q}/issues/{plan['issue_number']}/comments", {"body": recovery_comment(subject, rec)})
    api.patch(f"/repos/{q}/issues/{plan['issue_number']}", {"state": "closed", "state_reason": "completed"})
    return {**plan, "applied": True, "standing": "CLOSED[RECOVERY_RECEIPT]"}


def dedupe_demands(items: list[Observation]) -> list[Observation]:
    """Keep only the newest repair-demand candidate per subject fingerprint; order is preserved."""
    seen, out = set(), []
    for item in items:
        if item.action == "manufacture-repair-demand":
            fp = fingerprint(item)
            if fp in seen:
                continue
            seen.add(fp)
        out.append(item)
    return out


def token_for(repo: str, current_repo: str) -> tuple[str | None, str]:
    return ((os.environ.get("GITHUB_TOKEN"), "GITHUB_TOKEN") if repo == current_repo
            else (os.environ.get("MACRO_GITHUB_TOKEN"), "MACRO_GITHUB_TOKEN"))


def repair_body(item: Observation) -> str:
    fp = fingerprint(item)
    subject = subject_of(item)
    marker = json.dumps(dataclasses.asdict(subject), sort_keys=True, separators=(",", ":"))
    return f"""Authority: implementation

Manufactured by the GitHub macro governor from exact production evidence.

- source repository: `{item.repo}`
- source identity: `{item.identity}`
- source URL: {item.url}
- workflow: `{subject.workflow_name}` (id `{subject.workflow_id if subject.workflow_id is not None else 'UNKNOWN'}`)
- head SHA: `{item.metadata.get('head_sha') or 'UNKNOWN'}`
- conclusion: `{item.metadata.get('conclusion') or 'UNKNOWN'}`

Demand key: subject `(repo, workflow, head_sha, conclusion)`; later failing runs of the same subject
do not open new demands. Closes only on a success run of the same workflow on a descendant head.

Required loop:
`inspect -> reproduce -> RCA -> repair authoritative input -> exact-head Chicago -> receipt -> merge/containment -> permanent guard`

Do not blindly rerun deterministic product defects. Do not edit generated ownership surfaces.

<!-- macro-fingerprint:{fp} -->
<!-- macro-subject:{marker} -->
"""


def existing_demand(item: Observation, open_issues: list[dict[str, Any]]) -> Any:
    """Issue number of an open demand for the same subject (v2 fingerprint or legacy body)."""
    needle, subject = f"<!-- macro-fingerprint:{fingerprint(item)} -->", subject_of(item)
    for issue in open_issues:
        if "pull_request" in issue:
            continue
        if needle in str(issue.get("body") or ""):
            return issue.get("number")
        other = subject_of_issue(issue, item.repo)
        if other is not None and subject.same_subject(other):
            return issue.get("number")
    return None


def make_repair_demand(item: Observation, current_repo: str, apply: bool) -> dict[str, Any]:
    fp = fingerprint(item)
    result = {"action": "manufacture-repair-demand", "target": item.repo, "fingerprint": fp, "applied": False}
    if not apply:
        return {**result, "standing": "PLANNED"}
    token, name = token_for(item.repo, current_repo)
    if not token:
        return {**result, "standing": f"BLOCKED[{name}_MISSING]"}
    api, q = GitHub(token), urllib.parse.quote(item.repo, safe="/")
    existing = existing_demand(item, api.get(f"/repos/{q}/issues?state=open&per_page=100"))
    if existing is not None:
        return {**result, "standing": "NOOP[DEMAND_ALREADY_EXISTS]", "issue_number": existing}
    created = api.post(f"/repos/{q}/issues", {
        "title": f"[capability][repair] {item.title}: {item.metadata.get('conclusion') or 'abnormality'}",
        "body": repair_body(item),
    })
    return {**result, "applied": True, "standing": "ALIVE[REPAIR_DEMAND_CREATED]",
            "issue_number": created.get("number"), "issue_url": created.get("html_url")}


def rerun(item: Observation, current_repo: str, apply: bool) -> dict[str, Any]:
    result = {"action": "rerun-failed", "target": item.repo, "run_id": item.metadata["run_id"], "applied": False}
    if not apply:
        return {**result, "standing": "PLANNED"}
    if int(item.metadata.get("run_attempt") or 1) > 1:
        escalated = dataclasses.replace(item, action="manufacture-repair-demand",
                                       metadata={**item.metadata, "conclusion": "timed_out_after_retry"})
        return {**result, "standing": "ESCALATE[RETRY_BUDGET_EXHAUSTED]",
                "fallback": make_repair_demand(escalated, current_repo, apply)}
    token, name = token_for(item.repo, current_repo)
    if not token:
        return {**result, "standing": f"BLOCKED[{name}_MISSING]"}
    GitHub(token).post(f"/repos/{urllib.parse.quote(item.repo, safe='/')}/actions/runs/{item.metadata['run_id']}/rerun-failed-jobs")
    return {**result, "applied": True, "standing": "ALIVE[RERUN_REQUESTED]"}


def agent_prompt(item: Observation) -> str:
    return f"""Implement {item.repo} issue #{item.metadata['issue_number']}: {item.title}

{item.metadata.get('body') or ''}

Production contract:
- Repository doctrine and authority rules are binding.
- Prefer ontology/spec/ggen-marketplace/ggen manufacture over handwritten projections.
- Preserve DfCM alternatives until selection is justified.
- PragProg TPS is standard work.
- Execute the exact changed subject; failure is evidence.
- RCA -> repair -> reexecute; convert learning to permanent guard.
- Do not claim ALIVE from CI status alone.
- Open a PR with exact-head evidence.
- Do not ask a named operator what to do next when a lawful bounded path exists.
"""


def delegate(item: Observation, policy: Policy, apply: bool) -> dict[str, Any]:
    result = {"action": "delegate-agent", "target": item.repo,
              "issue_number": item.metadata["issue_number"], "applied": False}
    if not apply:
        return {**result, "standing": "PLANNED"}
    token = os.environ.get("COPILOT_AGENT_TOKEN")
    if not token:
        return {**result, "standing": "BLOCKED[COPILOT_AGENT_TOKEN_MISSING]"}
    api, q = GitHub(token), urllib.parse.quote(item.repo, safe="/")
    comments = api.get(f"/repos/{q}/issues/{item.metadata['issue_number']}/comments?per_page=100")
    if any("<!-- macro-agent-task:" in str(c.get("body") or "") for c in comments):
        return {**result, "standing": "NOOP[AGENT_ALREADY_DELEGATED]"}
    owner, repo = item.repo.split("/", 1)
    body = {"prompt": agent_prompt(item), "model": policy.agent_model,
            "create_pull_request": True, "base_ref": "main"}
    if policy.agent_custom_agent:
        body["custom_agent"] = policy.agent_custom_agent
    task = api.post(f"/agents/repos/{owner}/{repo}/tasks", body)
    api.post(f"/repos/{q}/issues/{item.metadata['issue_number']}/comments", {
        "body": f"Macro governor delegated this demand to GitHub Copilot agent task `{task.get('id')}`.\n\nTask: {task.get('html_url')}\n\n<!-- macro-agent-task:{task.get('id')} -->"
    })
    return {**result, "applied": True, "standing": "ALIVE[AGENT_TASK_STARTED]",
            "task_id": task.get("id"), "task_url": task.get("html_url")}


def execute(item: Observation, policy: Policy, current_repo: str, apply: bool) -> dict[str, Any]:
    if item.action == "rerun-failed":
        return rerun(item, current_repo, apply)
    if item.action == "manufacture-repair-demand":
        return make_repair_demand(item, current_repo, apply)
    if item.action == "delegate-agent":
        return delegate(item, policy, apply)
    return {"action": item.action, "target": item.repo, "applied": False, "standing": "NOOP[OBSERVATION_ONLY]"}


def write_receipt(path: Path, policy_path: Path, observations: list[Observation],
                  decisions: list[dict[str, Any]], started: dt.datetime, apply: bool,
                  errors: list[dict[str, str]]) -> None:
    doc = {
        "schema": "https://ggen.dev/receipts/github-macro-governor/v1",
        "repository": os.environ.get("GITHUB_REPOSITORY", ""),
        "source_sha": os.environ.get("GITHUB_SHA", ""),
        "run_id": os.environ.get("GITHUB_RUN_ID", ""),
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT", ""),
        "mode": "apply" if apply else "plan",
        "selection": "reverse-chronological-newest-unresolved-first",
        "started_at": started.isoformat(), "completed_at": now().isoformat(),
        "policy_path": str(policy_path),
        "policy_sha256": hashlib.sha256(policy_path.read_bytes()).hexdigest(),
        "observation_count": len(observations),
        "actionable_count": sum(actionable(x) for x in observations),
        "frontier": [dataclasses.asdict(x) for x in observations],
        "decisions": decisions, "collection_errors": errors,
    }
    text = json.dumps(doc, indent=2, sort_keys=True) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.with_suffix(path.suffix + ".sha256").write_text(
        f"{hashlib.sha256(text.encode()).hexdigest()}  {path.name}\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--policy", type=Path, default=Path("macro/governor.toml"))
    ap.add_argument("--receipt", type=Path, default=Path("macro/receipt.json"))
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--repo", action="append", default=[])
    args = ap.parse_args(argv)

    started, policy = now(), load_policy(args.policy)
    if args.repo:
        scope = set(args.repo)
        policy = dataclasses.replace(policy, managed=tuple(r for r in policy.managed if r.full_name in scope))
        if not policy.managed:
            raise SystemExit("REFUSED[NO_CONFIGURED_REPOSITORY_SELECTED]")

    current_repo = os.environ.get("GITHUB_REPOSITORY", "seanchatmangpt/ggen-ecosystem")
    api = GitHub(os.environ.get("MACRO_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN"))
    observations, errors = [], []
    reconciliations: list[dict[str, Any]] = []
    current = now()
    ancestry = GitHubAncestry(api)
    for repo in policy.managed:
        try:
            observations.extend(collect(api, repo, policy, current))
        except Exception as exc:
            errors.append({"repo": repo.full_name, "error": str(exc)})
            continue
        try:
            reconciliations.extend(collect_reconciliations(api, repo, policy, ancestry))
        except Exception as exc:
            errors.append({"repo": repo.full_name, "error": f"reconcile: {exc}"})

    observations = reverse_chronological(observations)
    candidates = dedupe_demands([x for x in observations if actionable(x)])
    recovered = {(p["target"], p["issue_number"]) for p in reconciliations if p["action"] == "close-on-recovery"}
    decisions = []
    for item in candidates[:max(0, policy.max_actions_per_run)]:
        if item.action == "delegate-agent" and (item.repo, item.metadata.get("issue_number")) in recovered:
            decisions.append({"action": item.action, "target": item.repo, "applied": False,
                              "issue_number": item.metadata.get("issue_number"),
                              "standing": "NOOP[DEMAND_RECOVERED]",
                              "source": {"kind": item.kind, "identity": item.identity,
                                         "updated_at": item.updated_at, "url": item.url}})
            continue
        try:
            decision = execute(item, policy, current_repo, args.apply)
        except Exception as exc:
            decision = {"action": item.action, "target": item.repo, "applied": False,
                        "standing": "BUILD_BROKEN[MACRO_ACTION_EXCEPTION]", "error": str(exc)}
        decision["source"] = {"kind": item.kind, "identity": item.identity,
                              "updated_at": item.updated_at, "url": item.url}
        decisions.append(decision)

    closes = 0
    for plan in reconciliations:
        if plan["action"] == "close-on-recovery":
            if closes >= max(0, policy.max_actions_per_run):
                plan = {**plan, "standing": "DEFERRED[ACTION_BUDGET_EXHAUSTED]"}
            else:
                closes += 1
                try:
                    plan = apply_recovery_close(plan, current_repo, args.apply)
                except Exception as exc:
                    plan = {**plan, "applied": False, "standing": "BUILD_BROKEN[MACRO_ACTION_EXCEPTION]",
                            "error": str(exc)}
        decisions.append(plan)

    write_receipt(args.receipt, args.policy, observations, decisions, started, args.apply, errors)
    summary = {
        "standing": "ALIVE" if not errors else "PARTIAL_ALIVE",
        "mode": "apply" if args.apply else "plan",
        "observations": len(observations), "actionable": len(candidates),
        "acted": sum(bool(d.get("applied")) for d in decisions),
        "decisions": len(decisions), "collection_errors": len(errors),
        "receipt": str(args.receipt),
    }
    print(json.dumps(summary, sort_keys=True))
    return 2 if any(str(d.get("standing", "")).startswith("BUILD_BROKEN") for d in decisions) else 0


if __name__ == "__main__":
    raise SystemExit(main())
