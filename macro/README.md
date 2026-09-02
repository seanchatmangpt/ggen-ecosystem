# GitHub Macro Autonomic Governor

This is the macro control plane **above** repository-local workflows, PRs, issues, crown reconciliation, and container publication.

## Control equation

```text
GitHub observations across managed repositories
  -> newest unresolved exact evidence first
  -> preserve older unsuperseded alternatives
  -> select smallest lawful action
  -> bounded actuation
  -> exact receipt
  -> next CapabilityDemand
```

The governor does not treat freshness as authority. It sorts unresolved evidence by `updated_at DESC`, then applies authority and action-budget gates.

## Inputs

`macro/governor.toml` is the canonical managed-repository/policy inventory.

`macro/ontology.ttl` defines the macro control laws:

- observation never gains DO authority;
- SELECT/CONSTRUCT/EXECUTE/VERIFY/RECEIPT remain distinct;
- cross-repository writes require an explicit token;
- one timed-out workflow gets at most one automatic rerun;
- deterministic workflow failures manufacture repair demand;
- `[capability]` issues are pull signals only from admitted authors;
- Copilot agent tasks are optional bounded workers, never merge authority;
- the prohibited terminal state is asking a named operator what to do next.

## Worker authority

The normal Actions `GITHUB_TOKEN` is sufficient for read access and same-repository issue/action operations.

Two optional secrets expand the authority envelope:

- `MACRO_GITHUB_TOKEN`: cross-repository issue/action mutation. Without it, external mutations become typed `BLOCKED[MACRO_GITHUB_TOKEN_MISSING]` decisions in the receipt.
- `COPILOT_AGENT_TOKEN`: user/fine-grained token with GitHub Agent Tasks permission. GitHub's agent-task API does not accept the Actions installation token. Without it, delegation becomes `BLOCKED[COPILOT_AGENT_TOKEN_MISSING]`.

Missing authority is not silently substituted.

## Abnormality policy

| Observation | Macro response |
|---|---|
| workflow success | closed; not in unresolved frontier |
| workflow running/queued | observe only |
| first `timed_out` run | rerun failed jobs once |
| second timeout | manufacture repair demand |
| deterministic `failure` | manufacture repair demand |
| authorized `[capability]` issue | delegate bounded agent when token exists |
| open PR | observe only; repository-local courts retain merge authority |

## Scheduling

`.github/workflows/github-macro-governor.yml` runs:

- every 15 minutes at `:13/:28/:43/:58` Pacific;
- after key local control workflows complete;
- on capability issue events;
- on explicit `repository_dispatch` macro signals;
- manually via `workflow_dispatch`;
- read-only on PRs that change the governor itself.

Concurrency cancels stale governor WIP. Every run uploads a full ordered frontier plus decisions and a SHA-256-bound receipt.

## Relationship to crowns

Repo-local crown/container workflows remain the fast deterministic control loops for exact dependency and image freshness.

The macro governor is the slower portfolio layer that asks:

> Across the ecosystem, what is the newest unresolved production evidence, and what is the narrowest lawful next act?

It therefore coordinates rather than replacing `Autonomic Crown`, `Container Freshness`, PragProg TPS, operator redundancy, Chicago courts, or downstream `gym-ecosystem` composition.
