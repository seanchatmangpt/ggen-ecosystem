# v26.9.15 — ggen-ecosystem: crown propagation behaving correctly

- **Date**: 2026-09-15
- **Source**: 14-hour cross-repo code review, window Sep 14 9:40 PM PDT → Sep 15 11:40 AM PDT.
- **Method**: inspection of commits, PR heads, and exact source files. No code executed, nothing changed by the reviewer.

## Result

`92356bd…` advances the marketplace pin from `861f098…` to `a241937…`. Crucially, it does **not** pretend the existing published `v26.9.10` container now contains that newer marketplace state. The lock retains:

- `standing = "BLOCKED"`
- `requires_republish = true`
- an explicit reason that the marketplace pin postdates the observed container build.

That is correct evidence propagation: the graph is ahead of the container, and the lock says so rather than crowning the newer graph through an older binary. No defect found.

## Tickets

| ID                                                                        | Title                                                                   | Severity    |
| ------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ----------- |
| [GECO-2601](./GECO-2601-crown-propagation-standing-retained.md)           | Marketplace pin advanced with container `BLOCKED` retained — correct     | Info (closed) |
