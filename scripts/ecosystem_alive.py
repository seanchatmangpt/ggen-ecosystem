#!/usr/bin/env python3
"""Evidence-preserving closure planner for the ggen ecosystem."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Callable, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
ALIVE = "ALIVE"
SAFE = "SAFE_REVERSIBLE"
AUTHORITY = "AUTHORITY_REQUIRED"

_IMMUTABLE_CAPSULE = re.compile(r"^.+@sha256:[0-9a-fA-F]{64}$")
_GENERATED_WORKFLOW_PREFIX = ".github/workflows/"
_GENERATED_WORKFLOW_SUFFIXES = (".yml", ".yaml")
_AUTHORITATIVE_GENERATOR_INPUTS = (
    "ontology.ttl",
    "ggen.toml",
    "ggen.lock",
    "ontology/",
    "vendor/ggen-marketplace/",
)


def admit_capsule_identity(reference: str, *, available: bool) -> dict:
    """Admit only an immutable, presently resolvable OCI capsule identity."""
    if not _IMMUTABLE_CAPSULE.fullmatch(reference):
        return {"standing": "REFUSED[MUTABLE_CAPSULE_IDENTITY]", "reference": reference}
    if not available:
        return {"standing": "REFUSED[CAPSULE_IDENTITY_UNAVAILABLE]", "reference": reference}
    return {"standing": ALIVE, "reference": reference}


def _is_generated_workflow(path: str) -> bool:
    return path.startswith(_GENERATED_WORKFLOW_PREFIX) and path.endswith(_GENERATED_WORKFLOW_SUFFIXES)


def _is_authoritative_generator_input(path: str) -> bool:
    return any(path == prefix or path.startswith(prefix) for prefix in _AUTHORITATIVE_GENERATOR_INPUTS)


def admit_projection_change(paths: Iterable[str]) -> dict:
    """Reject direct edits to generated workflows without an authoritative source delta."""
    normalized = tuple(sorted(set(paths)))
    generated = tuple(path for path in normalized if _is_generated_workflow(path))
    if generated and not any(_is_authoritative_generator_input(path) for path in normalized):
        return {
            "standing": "REFUSED[GENERATED_PROJECTION_DIRECT_EDIT]",
            "generated": generated,
            "paths": normalized,
        }
    return {"standing": ALIVE, "generated": generated, "paths": normalized}


def select_consumer_execution(*, container_available: bool, host_available: bool) -> dict:
    """Choose the strongest available stranger-journey execution surface deterministically."""
    if container_available:
        return {"standing": ALIVE, "route": "container"}
    if host_available:
        return {"standing": ALIVE, "route": "host"}
    return {"standing": "UNSUPPORTED[NO_CONSUMER_EXECUTION_SURFACE]", "route": None}


def run_doctor_sensor() -> dict:
    proc = subprocess.run(
        ["bash", str(REPO_ROOT / "scripts" / "doctor.sh"), "--json"],
        cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line.startswith("{") and line.endswith("}"):
            try:
                payload = json.loads(line)
                if isinstance(payload, dict):
                    return payload
            except json.JSONDecodeError:
                continue
    return {"subject": "seanchatmangpt/ggen-ecosystem", "fail": 1, "gates": [],
            "standing": "BUILD_BROKEN", "detail": "doctor emitted no valid JSON"}


def _step(action: list[str], cost: int, description: str, *, authority: str | None = None) -> dict:
    return {"argv": action, "action": " ".join(action),
            "type": AUTHORITY if authority else SAFE, "cost": cost,
            "description": description, **({"authority_token": authority} if authority else {})}


def plan_closure_autofde(gates: list[dict]) -> dict:
    by_name = {g.get("gate"): g for g in gates if isinstance(g, dict)}
    steps: list[dict] = []
    if by_name.get("1-submodules", {}).get("standing") not in (None, ALIVE):
        steps.append(_step(["git", "submodule", "update", "--init", "--recursive"], 2,
                           "Initialize and sync git submodules"))
    if by_name.get("9-workflow-drift", {}).get("standing") not in (None, ALIVE):
        steps.append(_step(["ggen", "sync", "run"], 1,
                           "Regenerate workflow projections via GGen"))
    if by_name.get("11-image-presence", {}).get("standing") not in (None, ALIVE):
        steps.append(_step(["docker", "build", "-t", "ggen-ecosystem:test", "."], 5,
                           "Build local container substrate"))
    if by_name.get("12-fresh-consumer", {}).get("standing") not in (None, ALIVE):
        host_runner = REPO_ROOT / "tests" / "run-fresh-consumer-host.sh"
        if host_runner.exists():
            steps.append(_step(["bash", str(host_runner.relative_to(REPO_ROOT))], 1,
                               "Verify fresh consumer crown through canonical host fallback"))
        else:
            steps.append(_step(["bash", "tests/run-fresh-consumer.sh", "ggen-ecosystem:test"], 2,
                               "Verify fresh consumer crown"))
    if by_name.get("13-image-publication", {}).get("standing") not in (None, ALIVE):
        steps.append(_step(["docker", "push", "ghcr.io/seanchatmangpt/ggen-ecosystem:v26.8.28"], 10,
                           "Publish release container to GitHub Container Registry",
                           authority="packages:write"))
    ordered = sorted(enumerate(steps), key=lambda item: (item[1]["type"] == AUTHORITY, item[1]["cost"], item[0]))
    steps = [step for _, step in ordered]
    non_alive = [g for g in gates if isinstance(g, dict) and g.get("standing") != ALIVE]
    return {"status": ALIVE if gates and not non_alive else "PARTIAL_ALIVE",
            "steps": steps, "total_cost": sum(s["cost"] for s in steps)}


def execute_safe_steps(plan: dict, runner: Callable[..., subprocess.CompletedProcess] = subprocess.run) -> dict:
    receipts = []
    for step in plan.get("steps", []):
        if step.get("type") != SAFE:
            continue
        proc = runner(step["argv"], cwd=REPO_ROOT, text=True,
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        receipt = {"action": step["action"], "argv": step["argv"], "exit": proc.returncode,
                   "stdout": proc.stdout, "stderr": proc.stderr,
                   "standing": ALIVE if proc.returncode == 0 else "BUILD_BROKEN"}
        receipts.append(receipt)
        if proc.returncode != 0:
            break
    return {"standing": ALIVE if receipts and all(r["exit"] == 0 for r in receipts) else
                        ("BUILD_BROKEN" if receipts else "PARTIAL_ALIVE"),
            "receipts": receipts}


def main() -> int:
    parser = argparse.ArgumentParser(description="Universal ALIVE interface for ggen-ecosystem.")
    parser.add_argument("--explain", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--apply-safe", action="store_true")
    args = parser.parse_args()
    sensor = run_doctor_sensor()
    plan = plan_closure_autofde(sensor.get("gates", []))
    if args.apply_safe:
        execution = execute_safe_steps(plan)
        print(json.dumps({"sensor": sensor, "closure_plan": plan, "execution": execution}, indent=2))
        return 0 if execution["standing"] in (ALIVE, "PARTIAL_ALIVE") else 1
    if args.json:
        print(json.dumps({"sensor": sensor, "closure_plan": plan,
                          "standing": ALIVE if not sensor.get("fail") else "PARTIAL_ALIVE"}, indent=2))
        return 0
    if args.next:
        print("NO OTHER WORK REMAINS" if not plan["steps"] else
              f"NEXT: {plan['steps'][0]['description']} [{plan['steps'][0]['type']}] -> {plan['steps'][0]['action']}")
        return 0
    print(f"SUBJECT: {sensor.get('subject', 'seanchatmangpt/ggen-ecosystem')}")
    print(f"CURRENT STANDING: {plan['status']}")
    if args.explain:
        for gate in sensor.get("gates", []):
            print(f"[{gate.get('standing', 'UNKNOWN')}] {gate.get('gate', 'unnamed')}: {gate.get('detail', '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
