# MFact certification plane

`mfact` contributes a **certification and standing court** to `ggen-ecosystem`.
It is not another generator, deployment engine, or source of ambient authority.

The ecosystem already has deterministic manufacture, producer pinning, receipts,
replay, Chicago qualification, and BRCE-bounded actuation. The missing reusable
mfact capability is the layer that answers a different question:

> Given the artifacts and receipts that exist, what standing may this exact
> subject lawfully claim?

## Imported invariants

The implementation adapts the public `seanchatmangpt/mfact` doctrine at exact
source `8a62a7c28e935b9afd05c68f455f475423ec0a7a`:

1. **Authority comes from an artifact ledger, not path names.**
   `certification/artifacts.toml` classifies source, projection, constructor,
   control, evidence, documentation, and verifier surfaces explicitly.
2. **Generated artifacts cannot confer standing.**
   The two GGen-manufactured workflows are projections and are mechanically
   refused if the ledger grants them standing authority.
3. **Producer identity must close.**
   GGen, Marketplace, git-submodule pins, release tag, GHCR repository, and
   immutable container digest must agree with `ecosystem.lock.toml`.
4. **Receipt identity must close.**
   The release receipt's GGen SHA, Marketplace SHA, container digest, admission,
   execution exit, and standing vocabulary must agree with the current lock.
5. **Historical evidence stays historical.**
   A valid receipt for an ancestor remains useful evidence, but it cannot promote
   a newer head to `ALIVE`. Changed load-bearing manufacturing paths are listed
   explicitly in the certification receipt.
6. **Standing promotion is fail-closed.**
   Contradictory producer/evidence/ledger identities produce a typed `REFUSED`.
   `--require-alive` turns any lower standing into a failing release gate.

## Authority separation

```text
ontology / ggen.toml       source authority
          |
          v
ggen sync run              CONSTRUCT
          |
          v
generated workflows        projection; no standing authority
          |
          v
execution receipts         evidence
          |
          v
mfact certification court  VERIFY only
          |
          v
scoped standing            UNKNOWN | PARTIAL_ALIVE | ALIVE | typed failure
```

The court never receives `DO`. BRCE remains the only consequential actuation
boundary.

## Operator surface

```bash
just certify-test
just certify
```

To emit a machine-readable receipt:

```bash
python3 scripts/certify_ecosystem.py \
  --root . \
  --receipt /tmp/mfact-certification.json
```

To make exact-head `ALIVE` mandatory for a release decision:

```bash
python3 scripts/certify_ecosystem.py --root . --require-alive
```

The default `just certify` is intentionally observational: a coherent
`PARTIAL_ALIVE` result exits successfully because bounded evidence is not a
broken certification system. Contradictory evidence exits non-zero.

## GitHub court

`.github/workflows/mfact-certification.yml` runs on relevant pull requests,
relevant `main` changes, and manual replay. It has `contents: read` only. The
workflow:

1. checks out the exact subject with full ancestry;
2. asserts exact-head identity;
3. runs the adversarial promotion/refusal unit suite;
4. executes the certification court;
5. preserves the JSON certification receipt as a GitHub Actions artifact;
6. refuses any verifier-induced repository mutation.

This workflow is an **independent verifier**, not one of the GGen-manufactured
workflow projections. Changes to the two manufactured ecosystem workflows still
belong in their ontology/pack source and must be regenerated through GGen.

## What is deliberately not imported

- mfact's Lean theorem corpus;
- process-intelligence algorithms;
- mfact release counts or theorem standing;
- mfact's local filesystem paths;
- a new deployment or merge authority;
- a new Marketplace pack.

Those are repository-specific. The reusable contribution is the certification
algebra: explicit artifact authority, exact evidence closure, anti-promotion
guards, lineage-aware standing, and replayable certification receipts.
