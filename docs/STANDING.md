# Standing and evidence

## Vocabulary

- `UNKNOWN` — required observation absent, stale, or contradictory.
- `PARTIAL_ALIVE` — bounded checkpoint executed successfully; crown claim remains open.
- `ALIVE` — observed execution against the exact admitted subject produced the claimed consequence.
- `BLOCKED` — an admitted dependency prevents the relevant execution.
- `BUILD_BROKEN` — the verifier cannot currently be reached because the build boundary is broken.
- `UNSUPPORTED` — outside the admitted capability boundary.
- `REFUSED:<type>` — admission deliberately denies a proposed state or action.

## Evidence dimensions

Track separately:
`observed`, `admitted`, `executed`, `changed`, `verified`, `inferred`, `refused`, `blocked`, `unsupported`.

A green workflow is evidence only for the exact commit and exact jobs that ran. A workflow file is not evidence that it ran.

The root claim may become `ALIVE` only after:
1. exact lock identities are materialized,
2. `ggen sync run` executes,
3. generated verifier(s) execute where applicable,
4. `ggen receipt verify` succeeds,
5. a second sync establishes deterministic replay/idempotence,
6. the exact subject SHA is bound into the resulting receipt/evidence chain.
