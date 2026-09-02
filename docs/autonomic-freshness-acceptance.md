# Freshness acceptance conditions

The autonomic freshness rail is ALIVE only when all of the following hold on the exact candidate:

- the candidate changes only admitted submodule Gitlinks and their lock identities;
- repository provenance, gym-factory, operator-redundancy, Docker build-check, and diff checks pass;
- `origin/main` still equals the base SHA observed before reconciliation;
- promotion is a non-forced fast-forward to the exact candidate SHA;
- the exact promoted SHA is published through the canonical container workflow;
- the published image can be pulled and executed; and
- the closure receipt binds the base SHA, candidate/main SHA, publication run, and standing.

A moved `main`, failed court, publication failure, or unauthorized path is a refusal, never an overwrite or silent success.
