#!/usr/bin/env python3
"""Seven-day ecosystem frontier admission court.

Reads an exact-subject observation manifest, verifies authority/ownership
invariants, and optionally checks every pinned branch head against GitHub.
The court is VERIFY-only and never mutates another repository.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_CEILINGS = {"EVIDENCE", "CONSTRUCT", "VERIFY"}
CANONICAL_OWNER_ROLES = {
    "universal-laws-factory-e-and-qme-specification",
    "semantic-law-state-and-executable-qualification",
    "ash-graphlaw-projection",
    "virtual-knowledge-graph-observation",
    "prepared-effect-consequence-protocol",
    "cryptographic-evidence-and-standing",
    "process-evidence-owner",
    "runtime-composition-owner",
    "semantic-manufacture-owner",
    "product-consequence-constitution",
}


class Refusal(ValueError):
    pass


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Refusal("REFUSED[FRONTIER_MANIFEST_NOT_OBJECT]")
    return value


def require_sha(value: Any, label: str) -> str:
    text = str(value)
    if not SHA40.fullmatch(text):
        raise Refusal(f"REFUSED[FRONTIER_SHA]:{label}:{text}")
    return text


def validate(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema") != "https://ggen.dev/admission/frontier-intake/v1":
        raise Refusal("REFUSED[FRONTIER_SCHEMA]")
    if manifest.get("authority", {}).get("ceiling") != "VERIFY":
        raise Refusal("REFUSED[FRONTIER_AUTHORITY_CEILING]")
    if manifest.get("authority", {}).get("do_authority") is not False:
        raise Refusal("REFUSED[FRONTIER_DO_AUTHORITY]")

    owners = manifest.get("canonical_owners")
    donors = manifest.get("frontier_donors")
    if not isinstance(owners, list) or not owners:
        raise Refusal("REFUSED[FRONTIER_OWNERS_EMPTY]")
    if not isinstance(donors, list) or not donors:
        raise Refusal("REFUSED[FRONTIER_DONORS_EMPTY]")

    owner_names: set[str] = set()
    subjects: list[dict[str, str]] = []
    roles: set[str] = set()
    for item in owners:
        repo = str(item.get("repository", ""))
        branch = str(item.get("branch", ""))
        sha = require_sha(item.get("sha"), repo or "owner")
        role = str(item.get("role", ""))
        if not repo or not branch or not role:
            raise Refusal(f"REFUSED[FRONTIER_OWNER_IDENTITY]:{repo}")
        if repo in owner_names:
            raise Refusal(f"REFUSED[DUPLICATE_CANONICAL_OWNER]:{repo}")
        owner_names.add(repo)
        roles.add(role)
        subjects.append({"repository": repo, "branch": branch, "sha": sha, "kind": "owner"})

    missing_roles = sorted(CANONICAL_OWNER_ROLES - roles)
    if missing_roles:
        raise Refusal("REFUSED[FRONTIER_OWNER_ROLE_CLOSURE]:" + ",".join(missing_roles))

    donor_names: set[str] = set()
    for item in donors:
        repo = str(item.get("repository", ""))
        branch = str(item.get("branch", ""))
        sha = require_sha(item.get("sha"), repo or "donor")
        target = str(item.get("target_owner", ""))
        ceiling = str(item.get("authority_ceiling", ""))
        capability = str(item.get("capability", ""))
        if not repo or not branch or not capability:
            raise Refusal(f"REFUSED[FRONTIER_DONOR_IDENTITY]:{repo}")
        if repo in donor_names:
            raise Refusal(f"REFUSED[DUPLICATE_FRONTIER_DONOR]:{repo}")
        if target not in owner_names:
            raise Refusal(f"REFUSED[FRONTIER_UNKNOWN_OWNER]:{repo}:{target}")
        if ceiling not in ALLOWED_CEILINGS:
            raise Refusal(f"REFUSED[FRONTIER_AUTHORITY]:{repo}:{ceiling}")
        if ceiling == "VERIFY":
            raise Refusal(f"REFUSED[DONOR_VERIFY_SOVEREIGNTY]:{repo}")
        donor_names.add(repo)
        subjects.append({"repository": repo, "branch": branch, "sha": sha, "kind": "donor"})

    falsifiers = manifest.get("falsifiers")
    if not isinstance(falsifiers, list) or len(falsifiers) < 8 or not all(isinstance(x, str) and x for x in falsifiers):
        raise Refusal("REFUSED[FRONTIER_FALSIFIER_COVERAGE]")

    return {
        "owner_count": len(owners),
        "donor_count": len(donors),
        "subjects": subjects,
        "falsifier_count": len(falsifiers),
    }


def github_head(repository: str, branch: str) -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ggen-ecosystem-frontier-intake/1",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    owner, repo = repository.split("/", 1)
    url = f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise Refusal(f"BLOCKED[FRONTIER_REMOTE_EVIDENCE]:{repository}:{branch}:{exc}") from exc
    return require_sha(payload.get("commit", {}).get("sha"), repository)


def observe_live(subjects: list[dict[str, str]]) -> list[dict[str, str]]:
    observations = []
    for subject in sorted(subjects, key=lambda x: (x["repository"], x["branch"])):
        actual = github_head(subject["repository"], subject["branch"])
        if actual != subject["sha"]:
            raise Refusal(
                f"REFUSED[FRONTIER_HEAD_DRIFT]:{subject['repository']}:{subject['sha']}:{actual}"
            )
        observations.append({**subject, "observed_head": actual, "standing": "ALIVE"})
    return observations


def run(manifest_path: Path, *, live: bool) -> dict[str, Any]:
    manifest = load(manifest_path)
    structural = validate(manifest)
    observed = observe_live(structural["subjects"]) if live else []
    return {
        "schema": "https://ggen.dev/receipts/frontier-intake/v1",
        "manifest": str(manifest_path),
        "window": manifest["window"],
        "target": manifest["target"],
        "authority": {"ceiling": "VERIFY", "do_authority": False},
        "owner_count": structural["owner_count"],
        "donor_count": structural["donor_count"],
        "falsifier_count": structural["falsifier_count"],
        "live": live,
        "observations": observed,
        "standing": "ALIVE",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="admission/frontier-2026-09-30.json")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--receipt")
    parser.add_argument("--require-alive", action="store_true")
    args = parser.parse_args(argv)

    try:
        result = run(Path(args.manifest), live=args.live)
        code = 0
    except (Refusal, OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {
            "schema": "https://ggen.dev/receipts/frontier-intake/v1",
            "authority": {"ceiling": "VERIFY", "do_authority": False},
            "standing": str(exc),
        }
        code = 2

    rendered = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.receipt:
        out = Path(args.receipt)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    if args.require_alive and result.get("standing") != "ALIVE":
        return 3
    return code


if __name__ == "__main__":
    raise SystemExit(main())
