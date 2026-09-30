#!/usr/bin/env python3
"""Exact-subject QME-1 cross-ecosystem qualification crown.

This verifier composes already-owned ecosystem capabilities. It does not copy
QME-1 normative law, grant authority, or promote the numerical marketplace
work-equivalent claim. It observes exact public GitHub subjects and successful
workflow evidence, then emits a replayable VERIFY-only receipt.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SHA40 = re.compile(r"^[0-9a-f]{40}$")
QME_PROFILE = "QME-1/EcosystemReference"
CANONICAL_QME_SUBJECT = (
    "seanchatmangpt/chatman-ecosystem@"
    "32c47032a9cefd0ab4f0980efc32fa84505031b2"
)
REQUIRED_INHERITANCE = frozenset(
    {
        "exact-subject",
        "canonical-ownership",
        "consequence-separation",
        "independent-observation",
        "replay-non-actuation",
        "negative-knowledge",
        "semantic-manufacture-provenance",
        "mxinf-fail-closed",
    }
)


class CrownRefusal(ValueError):
    """The exact-subject crown could not admit its evidence."""


def digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def require_sha(value: Any, label: str) -> str:
    text = str(value)
    if not SHA40.fullmatch(text):
        raise CrownRefusal(f"REFUSED[EXACT_SUBJECT_SHA]:{label}:{text}")
    return text


def exact_local_head(root: Path) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if proc.returncode != 0:
        raise CrownRefusal(f"REFUSED[LOCAL_HEAD_UNAVAILABLE]:{proc.stderr.strip()}")
    return require_sha(proc.stdout.strip(), "local_head")


def _request(url: str, *, accept: str | None = None) -> bytes:
    headers = {"User-Agent": "ggen-ecosystem-qme-crown/1"}
    if accept:
        headers["Accept"] = accept
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise CrownRefusal(f"BLOCKED[REMOTE_EVIDENCE_UNAVAILABLE]:{url}:{exc}") from exc


def fetch_raw(repository: str, sha: str, path: str) -> bytes:
    require_sha(sha, f"{repository}:{path}")
    owner, name = repository.split("/", 1)
    url = f"https://raw.githubusercontent.com/{owner}/{name}/{sha}/{path}"
    return _request(url)


def fetch_run(repository: str, run_id: int) -> dict[str, Any]:
    owner, name = repository.split("/", 1)
    raw = _request(
        f"https://api.github.com/repos/{owner}/{name}/actions/runs/{run_id}",
        accept="application/vnd.github+json",
    )
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CrownRefusal(f"REFUSED[WORKFLOW_EVIDENCE_INVALID_JSON]:{repository}:{run_id}") from exc
    if not isinstance(payload, dict):
        raise CrownRefusal(f"REFUSED[WORKFLOW_EVIDENCE_INVALID]:{repository}:{run_id}")
    return payload


def validate_profile(
    *,
    repository: str,
    sha: str,
    role: str,
    canonical_subject: str,
) -> dict[str, Any]:
    raw = fetch_raw(repository, sha, ".qme/profile.json")
    try:
        profile = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CrownRefusal(f"REFUSED[QME_PROFILE_INVALID_JSON]:{repository}@{sha}") from exc

    checks = {
        "qme_profile": profile.get("qme_profile") == QME_PROFILE,
        "canonical_spec_subject": profile.get("canonical_spec_subject") == canonical_subject,
        "role": profile.get("role") == role,
        "normative": profile.get("normative") is False,
        "weakens_core": profile.get("weakens_core") is False,
        "authority": profile.get("authority_granted_by_projection") == "none",
        "inheritance": REQUIRED_INHERITANCE.issubset(set(profile.get("inheritance", []))),
    }
    failed = sorted(name for name, ok in checks.items() if not ok)
    if failed:
        raise CrownRefusal(
            f"REFUSED[QME_PROFILE_CONFORMANCE]:{repository}@{sha}:{','.join(failed)}"
        )
    return {
        "repository": repository,
        "sha": sha,
        "role": role,
        "profile_sha256": digest(raw),
        "local_subject": profile.get("local_subject"),
        "authority_granted_by_projection": "none",
    }


def validate_workflow(
    *,
    repository: str,
    run_id: int,
    expected_name: str,
    expected_head_sha: str,
) -> dict[str, Any]:
    payload = fetch_run(repository, run_id)
    actual_name = payload.get("name")
    actual_head = payload.get("head_sha")
    status = payload.get("status")
    conclusion = payload.get("conclusion")
    event = payload.get("event")
    if actual_name != expected_name:
        raise CrownRefusal(
            f"REFUSED[WORKFLOW_NAME_DRIFT]:{repository}:{run_id}:{actual_name}"
        )
    if actual_head != expected_head_sha:
        raise CrownRefusal(
            f"REFUSED[WORKFLOW_SUBJECT_DRIFT]:{repository}:{run_id}:{actual_head}"
        )
    if status != "completed" or conclusion != "success":
        raise CrownRefusal(
            f"PARTIAL_ALIVE[WORKFLOW_NOT_SUCCESS]:{repository}:{run_id}:{status}:{conclusion}"
        )
    return {
        "repository": repository,
        "run_id": run_id,
        "name": actual_name,
        "head_sha": actual_head,
        "status": status,
        "conclusion": conclusion,
        "event": event,
        "html_url": payload.get("html_url"),
    }


def validate_canonical_spec(spec: dict[str, Any]) -> dict[str, Any]:
    repository = str(spec.get("repository", ""))
    sha = require_sha(spec.get("sha"), "canonical_spec")
    path = str(spec.get("path", ""))
    if not repository or not path:
        raise CrownRefusal("REFUSED[CANONICAL_SPEC_IDENTITY]")
    raw = fetch_raw(repository, sha, path)
    text = raw.decode("utf-8", errors="strict")
    required = (
        "# RFC QME-1",
        "Status: Draft Standard",
        "Authority: NONE",
        "qualification",
    )
    missing = [token for token in required if token not in text]
    if missing:
        raise CrownRefusal(
            f"REFUSED[CANONICAL_SPEC_CONTENT]:{repository}@{sha}:{','.join(missing)}"
        )
    return {
        "repository": repository,
        "sha": sha,
        "path": path,
        "sha256": digest(raw),
    }


def validate_qualification_engine(engine: dict[str, Any]) -> dict[str, Any]:
    repository = str(engine.get("repository", ""))
    sha = require_sha(engine.get("sha"), "qualification_engine")
    module_path = str(engine.get("module_path", ""))
    profile_path = str(engine.get("profile_path", ""))
    run_id = int(engine.get("workflow_run_id"))
    workflow_name = str(engine.get("workflow_name", ""))

    module = fetch_raw(repository, sha, module_path)
    profile = fetch_raw(repository, sha, profile_path)
    module_text = module.decode("utf-8", errors="strict")
    for symbol in (
        "pub fn evaluate",
        "pub fn generate_falsifier",
        "pub fn compose_courts",
        "pub fn temporal_rule_holds",
    ):
        if symbol not in module_text:
            raise CrownRefusal(
                f"REFUSED[QUALIFICATION_ENGINE_SURFACE]:{repository}@{sha}:{symbol}"
            )
    try:
        profile_json = json.loads(profile)
    except json.JSONDecodeError as exc:
        raise CrownRefusal(
            f"REFUSED[QUALIFICATION_PROFILE_INVALID]:{repository}@{sha}"
        ) from exc
    courts = profile_json.get("courts")
    if not isinstance(courts, list) or not courts:
        raise CrownRefusal(
            f"REFUSED[QUALIFICATION_PROFILE_EMPTY]:{repository}@{sha}"
        )
    run = validate_workflow(
        repository=repository,
        run_id=run_id,
        expected_name=workflow_name,
        expected_head_sha=sha,
    )
    return {
        "repository": repository,
        "sha": sha,
        "module_path": module_path,
        "module_sha256": digest(module),
        "profile_path": profile_path,
        "profile_sha256": digest(profile),
        "court_count": len(courts),
        "workflow": run,
        "authority": "NONE",
        "consequence": "EVIDENCE_ONLY",
    }


def validate_marketplace_claim(claim: dict[str, Any]) -> dict[str, Any]:
    repository = str(claim.get("marketplace_repository", ""))
    sha = require_sha(claim.get("marketplace_candidate_sha"), "marketplace_candidate")
    court_path = str(claim.get("court_path", ""))
    ledger_path = str(claim.get("ledger_path", ""))
    workflow_path = str(claim.get("workflow_path", ""))
    target = claim.get("target_person_years")
    expected_claim_standing = str(claim.get("expected_claim_standing", ""))

    court = fetch_raw(repository, sha, court_path)
    ledger_raw = fetch_raw(repository, sha, ledger_path)
    workflow = fetch_raw(repository, sha, workflow_path)
    try:
        ledger = json.loads(ledger_raw)
    except json.JSONDecodeError as exc:
        raise CrownRefusal(
            f"REFUSED[MARKETPLACE_LEDGER_INVALID]:{repository}@{sha}"
        ) from exc

    ledger_target = ledger.get("claim", {}).get("person_years")
    if target != 500_000_000 or ledger_target != target:
        raise CrownRefusal(
            f"REFUSED[MARKETPLACE_TARGET_DRIFT]:manifest={target}:ledger={ledger_target}"
        )
    evidence = ledger.get("evidence")
    if not isinstance(evidence, list):
        raise CrownRefusal("REFUSED[MARKETPLACE_EVIDENCE_NOT_ARRAY]")
    if expected_claim_standing != (
        "UNSUPPORTED:INSUFFICIENT_INDEPENDENT_HUMAN_BASELINE_EVIDENCE"
    ):
        raise CrownRefusal("REFUSED[MARKETPLACE_CLAIM_STANDING_DRIFT]")

    court_text = court.decode("utf-8", errors="strict")
    for token in (
        "commit_count_is_not_person_years",
        "raw_combinatorics_is_not_person_years",
        "overlap_safe_hours",
        "UNSUPPORTED:INSUFFICIENT_INDEPENDENT_HUMAN_BASELINE_EVIDENCE",
    ):
        if token not in court_text:
            raise CrownRefusal(
                f"REFUSED[MARKETPLACE_COURT_SURFACE]:{repository}@{sha}:{token}"
            )

    run = validate_workflow(
        repository=repository,
        run_id=int(claim.get("workflow_run_id")),
        expected_name=str(claim.get("workflow_name", "")),
        expected_head_sha=sha,
    )
    return {
        "repository": repository,
        "sha": sha,
        "target_person_years": target,
        "evidence_items": len(evidence),
        "claim_standing": expected_claim_standing,
        "court_sha256": digest(court),
        "ledger_sha256": digest(ledger_raw),
        "workflow_sha256": digest(workflow),
        "workflow": run,
    }


def crown(root: Path, manifest_path: Path) -> dict[str, Any]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CrownRefusal(f"REFUSED[CROWN_MANIFEST_INVALID]:{exc}") from exc

    if manifest.get("schema_version") != 1:
        raise CrownRefusal("REFUSED[CROWN_SCHEMA_VERSION]")
    if manifest.get("court") != "QME-1/CrossEcosystem500MClaimCrown":
        raise CrownRefusal("REFUSED[CROWN_IDENTITY]")
    if manifest.get("authority_ceiling") != "VERIFY":
        raise CrownRefusal("REFUSED[CROWN_AUTHORITY_CEILING]")
    if manifest.get("claim_authority") != "NONE":
        raise CrownRefusal("REFUSED[CLAIM_AUTHORITY_ESCALATION]")

    canonical = validate_canonical_spec(manifest.get("canonical_spec", {}))
    canonical_subject = f"{canonical['repository']}@{canonical['sha']}"
    if canonical_subject != CANONICAL_QME_SUBJECT:
        raise CrownRefusal(
            f"REFUSED[CANONICAL_QME_SUBJECT_DRIFT]:{canonical_subject}"
        )

    participants_raw = manifest.get("participants")
    if not isinstance(participants_raw, list) or not participants_raw:
        raise CrownRefusal("REFUSED[PARTICIPANT_SET_EMPTY]")

    seen: set[str] = set()
    participants = []
    for item in participants_raw:
        repository = str(item.get("repository", ""))
        if repository in seen:
            raise CrownRefusal(f"REFUSED[DUPLICATE_PARTICIPANT]:{repository}")
        seen.add(repository)
        participants.append(
            validate_profile(
                repository=repository,
                sha=require_sha(item.get("sha"), repository),
                role=str(item.get("role", "")),
                canonical_subject=canonical_subject,
            )
        )

    engine = validate_qualification_engine(manifest.get("qualification_engine", {}))
    claim = validate_marketplace_claim(manifest.get("claim", {}))

    return {
        "schema": "https://ggen.dev/receipts/qme-1-cross-ecosystem-crown/v1",
        "court": manifest["court"],
        "subject": {
            "repository": "seanchatmangpt/ggen-ecosystem",
            "exact_head": exact_local_head(root),
        },
        "canonical_spec": canonical,
        "participants": participants,
        "qualification_engine": engine,
        "marketplace_claim": claim,
        "authority_ceiling": "VERIFY",
        "claim_authority": "NONE",
        "standing": "ALIVE",
        "claim_standing": claim["claim_standing"],
        "invariants": {
            "candidate_is_not_truth": True,
            "evidence_is_not_authority": True,
            "receipt_is_not_do": True,
            "replay_is_non_actuating": True,
            "numerical_claim_not_promoted": True,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--manifest",
        default="certification/qme-1-crown.json",
    )
    parser.add_argument("--receipt")
    parser.add_argument("--require-alive", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path

    try:
        result = crown(root, manifest_path)
        code = 0
    except CrownRefusal as exc:
        result = {
            "schema": "https://ggen.dev/receipts/qme-1-cross-ecosystem-crown/v1",
            "court": "QME-1/CrossEcosystem500MClaimCrown",
            "subject": {
                "repository": "seanchatmangpt/ggen-ecosystem",
                "exact_head": None,
            },
            "authority_ceiling": "VERIFY",
            "claim_authority": "NONE",
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
