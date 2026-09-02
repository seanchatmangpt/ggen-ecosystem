# Operator Redundancy

## Purpose

The system is not complete while a named human is its runtime control plane.

Operator redundancy separates **constitutional agency** from **operational execution**. Humans may define goals, values, identity-bound consent, and authority envelopes. Once those boundaries are admitted, ordinary operation must be observable, selectable, actuable, verifiable, recoverable, and receipted without depending on a particular person's memory or attention.

## Redundancy criterion

Let `D_operational` be the set of runtime dependencies for operational workflows and `D_named_human` the subset that require a named human.

```text
R_operator = 1 - |D_named_human| / |D_operational|
```

The operational target is `R_operator = 1`.

This does **not** mean removing human agency. It means moving human participation to an explicit constitutional boundary rather than allowing it to leak into runtime operations.

## Admission contract

Every `OperationalWorkflow` must declare:

1. an external observation source;
2. an executable decision policy;
3. a bounded authority envelope;
4. a non-human actuation path;
5. an independent verifier;
6. a receipt sink;
7. an executable recovery path;
8. `runtimeRequiresHuman false`;
9. `missingCapabilityPolicy ManufactureChildAndResume`.

Every `CapabilityRequest` must be handled by a `ChildManufactureWorkflow`. The child must have bounded authority, independent verification, receipts, no runtime human dependency, and a declared parent workflow to resume.

A `ConstitutionalDecision` may require a `HumanPrincipal`. Constitutional decisions are intentionally distinct from operational workflows.

## State machine

```text
OBSERVE
  -> SELECT under policy
  -> ACTUATE inside authority envelope
  -> VERIFY independently
  -> RECEIPT
  -> REPLAN

failure
  -> RECOVER
  -> VERIFY
  -> RECEIPT
  -> REPLAN

missing capability
  -> CAPABILITY REQUEST
  -> CHILD MANUFACTURE
  -> VERIFY CHILD
  -> PROMOTE/PIN
  -> RECEIPT
  -> RESUME PARENT
```

The prohibited terminal state is `ask a named operator what to do next` for an operational concern.

## Application surface

The invariant applies recursively to software manufacture, CI/release, security qualification, incident recovery, research/evaluation, work-portfolio management, recurring reporting, administrative intake, and any other repeated question or process that can be bounded by observable evidence and lawful authority.

A repeated operational question is a signal to manufacture a reusable evaluator, verifier, simulator, workflow, adapter, or service rather than repeatedly consume human attention.

## Court

`Operator Redundancy Court` uses the real `ggen-ecosystem` manufacturing wrapper against an exact-head, physically contained downstream vendor topology. It proves:

- an admitted operational workflow manufactures a redundancy receipt;
- a constitutional human boundary remains admissible;
- replay is deterministic;
- changed admitted intent changes the manufactured evidence;
- a runtime human dependency is refused by SHACL;
- a capability gap without a child manufacture-and-resume path is refused by SHACL.

Standing is emitted only as:

```text
OPERATOR_REDUNDANCY_CHICAGO_ALIVE
```

when the complete causal chain passes.
