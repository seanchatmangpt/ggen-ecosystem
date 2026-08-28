# Receipts

`receipts/` is documentation for ecosystem-level evidence. Runtime ggen receipts live under `.ggen-v2/` and are created by actual sync execution.

A receipt must bind:
- exact subject identity,
- admitted graph identity,
- manufacturer/toolchain identity,
- authority,
- consequence/output hashes,
- replay coordinates,
- standing scope.

Do not commit a fabricated receipt. A file named `receipt` is not evidence unless the matching verifier accepts it.
