# Macro Governor Demand Lifecycle

v26.9.26. Capability C17 / GGE-26922-14: subject-keyed demand with anti-windup, implemented in
`scripts/github_macro_governor.py` and qualified by `tests/test_github_macro_governor.py`.

## Demand key

A repair demand is keyed by its subject `(repo, workflow_id, head_sha, conclusion)`.
The run id is not part of the key. Three failing runs of one workflow on one head with one
conclusion yield one fingerprint (`fingerprint()`), one candidate per governor pass
(`dedupe_demands()`), and at most one open issue (`existing_demand()` returns
`NOOP[DEMAND_ALREADY_EXISTS]`). Legacy run-keyed issues (for example #365 and #366) are matched
by parsing their body fields and title, so they also suppress new duplicates.

New demand bodies carry two markers:

```text
<!-- macro-fingerprint:<24 hex> -->
<!-- macro-subject:{"conclusion":...,"head_sha":...,"observed_at":...,"repo":...,"workflow_id":...,"workflow_name":...} -->
```

## Close on recovery

`reconcile_demands()` examines every open governor demand in a managed repository. A demand is
planned `close-on-recovery` only when all of these hold:

1. A completed `success` run exists in the same repository for the same workflow (the same
   `workflow_id`, or the same workflow name for legacy demands that carry no id).
2. That run is newer than the demand (failure `observed_at`, or issue `created_at` for legacy).
3. The run's head descends from, or equals, the demand head. Production asks the GitHub
   compare API (`ahead` or `identical`); tests use a real git store through `git merge-base
   --is-ancestor`.

On apply, the governor posts a comment that cites the recovery run id
(`<!-- macro-recovery:<run id> -->`) and closes the issue. The receipt standing is
`CLOSED[RECOVERY_RECEIPT]`. A close plan without `recovery_run_id` is refused with
`REFUSED[NO_RECOVERY_RUN_ID]`.

Every other demand stays open: `OPEN[NO_RECOVERY_RECEIPT]`, or `OPEN[ANCESTRY_UNKNOWN]` when
ancestry cannot be decided. Delegation to an agent is skipped for a demand that is closing in the
same pass (`NOOP[DEMAND_RECOVERED]`). Closes are bounded by `max_actions_per_run`; the excess is
`DEFERRED[ACTION_BUDGET_EXHAUSTED]`.

## Falsifier

- One `(workflow, head_sha, conclusion)` produces more than one fingerprint across 3 failing runs.
- A demand closes without a descendant success run id in its receipt.

## See Also

- `docs/RECEIPT-SCHEMA.md`
- `docs/STANDING.md`
- `.github/workflows/github-macro-governor.yml`
