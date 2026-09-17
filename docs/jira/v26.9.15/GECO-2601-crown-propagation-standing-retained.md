# GECO-2601: Marketplace pin advanced with container `BLOCKED` retained — correct propagation

- **Status**: Closed (no action)
- **Severity**: Info
- **Found by**: 14-hour cross-repo code review, window 2026-09-14 9:40 PM → 2026-09-15 11:40 AM PDT (inspection, not execution)

## Evidence

`92356bd…` advances the marketplace pin from `861f098…` to `a241937…` while the lock retains:

- `standing = "BLOCKED"`
- `requires_republish = true`
- an explicit reason that the marketplace pin postdates the observed container build.

## Impact

Correct evidence propagation. The graph is ahead of the container, and the lock says so rather than crowning the newer graph through an older binary — the published `v26.9.10` container is not falsely credited with newer marketplace state.

## Fix

None required. Recorded as the reference behavior for crown propagation.
