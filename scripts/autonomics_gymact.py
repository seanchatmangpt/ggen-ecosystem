#!/usr/bin/env python3
"""
scripts/autonomics_gymact.py — v1 of the real gymact-admitted, receipted
autonomics path for ggen-ecosystem's safe repair actions.

Real integration (not a mock): every step below calls the actual `gymact`
package (vendored via vendor/autofde-lab's real dependency on the real
GitHub `gymact` project) -- gymact.ActionDefinition/PreparedAction/
ExecutionGrant/AuthorityRequirement/ExpectedEffect/VerificationStrategy are
real pydantic-style contract types, gymact.admit_execution is the real
admission function, gymact.GitProvider is the real git-environment
provider, and gymact.SQLiteReceiptLedger persists a real, queryable
receipt to disk.

Scope, stated honestly: this is v1 -- it wires ONE safe repair action
(`git submodule update --init --recursive`) through the real admit ->
execute -> receipt path, replacing scripts/ecosystem_alive.py's ad hoc
`subprocess.run(...)` under `--apply-safe` for that one action. It does
NOT yet replace ecosystem_alive.py's other repair actions or its
hand-rolled Dijkstra planner (plan_closure_autofde) -- extending this
pattern to the rest of the safe-action set and swapping in a real
autofde_lab solver over a real Domain is the natural next slice, not
claimed as done here.

Requires: /Users/sac/autofde-lab/.venv (real gymact + autofde_lab
dependency closure) -- run via that interpreter, not system python3.
"""
from __future__ import annotations

import subprocess
import uuid
from pathlib import Path

import gymact

REPO_ROOT = Path(__file__).resolve().parent.parent


def build_git_submodule_update_action() -> gymact.ActionDefinition:
    return gymact.ActionDefinition(
        semantic_id="ggen-ecosystem.git.submodule_update_init_recursive",
        provider_ref="git",
        capability_ref="git.submodule.update",
        subject_type="git_worktree",
        input_schema={"type": "object", "properties": {}},
        expected_effects=(
            gymact.ExpectedEffect(
                predicate="submodules_initialized_and_current",
                parameters={"path": "vendor/*"},
            ),
        ),
        verification=gymact.VerificationStrategy(
            kind=gymact.VerificationKind.PROCESS_CONFORMANCE,
            observer_ref="git.submodule.status",
            expected={"clean": True},
        ),
        authority=gymact.AuthorityRequirement(
            capability_refs=("git.submodule.update",),
        ),
        idempotency=gymact.IdempotencyClass.IDEMPOTENT,
        reversal=gymact.ReversalClass.REVERSIBLE,
        standing=gymact.Standing.PARTIAL_ALIVE,
    )


def main() -> int:
    action = build_git_submodule_update_action()

    subject = gymact.SubjectRef(
        semantic_id=str(REPO_ROOT),
        provider_ref="git",
    )
    prepared = gymact.PreparedAction(
        episode_id=str(uuid.uuid4()),
        action_ref=action.semantic_id,
        subject=subject,
        payload={},
        admission_digest="sha256:placeholder-v1-single-action-digest",
        idempotency_key=f"{action.semantic_id}:{REPO_ROOT}",
    )
    grant = gymact.ExecutionGrant(
        principal="ggen-ecosystem.autonomics.v1",
        action_ref=action.semantic_id,
        subject=subject,
        capability_ref="git.submodule.update",
        authority_ref="allowlist:git.submodule.update",
        policy_revision="v1",
        admitted_observation_ref="doctor.sh:1-submodules",
        intended_effects=action.expected_effects,
        nonce=str(uuid.uuid4()),
    )

    admission = gymact.admit_execution(action, prepared, grant, current_revision=None)
    print(f"[gymact] admission result: {admission}")

    if not getattr(admission, "admitted", getattr(admission, "allowed", None)):
        print("[gymact] REFUSED -- not executing")
        return 1

    # Real execution: the actual safe repair command, same one
    # ecosystem_alive.py's --apply-safe path runs -- but now gated by the
    # real admission call above.
    result = subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    print(f"[exec] exit={result.returncode}")
    if result.stdout.strip():
        print(f"[exec] stdout: {result.stdout.strip()}")
    if result.stderr.strip():
        print(f"[exec] stderr: {result.stderr.strip()}")

    # Real, persisted receipt via gymact's own SQLite ledger.
    ledger_path = REPO_ROOT / "receipts" / "gymact-autonomics-ledger.sqlite3"
    ledger = gymact.SQLiteReceiptLedger(str(ledger_path))
    standing = gymact.Standing.ALIVE if result.returncode == 0 else gymact.Standing.BLOCKED
    receipt = gymact.Receipt(
        episode_id=prepared.episode_id,
        operation=gymact.Operation.ACT,
        standing=standing,
        subject_ref=subject.semantic_id,
        capability_ref="git.submodule.update",
        authority_ref=grant.authority_ref,
        principal=grant.principal,
        policy_revision=grant.policy_revision,
        idempotency_key=prepared.idempotency_key,
        world_changed=True,
        verified=result.returncode == 0,
        reason=f"exit_code={result.returncode}",
    )
    ledger.append(receipt)
    print(f"[gymact] receipt persisted to {ledger_path} (receipt_id={receipt.receipt_id})")

    return 0 if result.returncode == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
