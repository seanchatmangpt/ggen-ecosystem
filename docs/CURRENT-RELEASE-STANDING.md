# Current release standing

This page is the canonical current release-standing correction for the composed `ggen-ecosystem` capsule. Older Definition-of-Done rows remain historical execution evidence and must not be interpreted as fresh availability claims after the exact subject changes.

## Exact admitted subject

- repository: `seanchatmangpt/ggen-ecosystem`
- reconciliation ancestor: `f42aa25c4974a0d5a701ed0e08f3bce46d69d115`
- ggen source: `c61ee99359c9dbc7b3cb71687976932a3e737ed4`
- marketplace source: `89adf4c8476f7edc8067fdbb1c256cfbfa22df6a`
- autofde-lab gitlink: `a4dbb9a9943d23b51af9f3dc71b7beba52b3ec09`

The current repository head must be resolved at verification time; the ancestor above records the reconciliation lineage, not a claim that future heads inherit execution evidence automatically.

## Capsule standing

`BLOCKED[GHCR_MANIFEST_UNKNOWN]`

The historical capsule identity
`ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c`
is preserved as provenance evidence, but a later GitHub-hosted replay (Actions run `33238309149`)
observed `manifest unknown` during job-container initialization. Therefore the digest is not a
currently admitted pullable execution capsule.

No release or consumer path may promote this digest to `ALIVE` from the historical successful
local/fresh-consumer observations alone. A replacement capsule must be published, resolved to an
immutable digest, pulled from a fresh consumer, executed, receipted, and replayed against the same
admitted identities.

The external execution crown is tracked by GitHub issue `#146`. Repository-local work may prepare and verify the path, but closing that issue requires observed publication and fresh consumer execution rather than configuration alone.

## Lock correspondence

`ecosystem.lock.toml` is required to match the repository gitlinks. In particular,
`[submodules].autofde_lab_commit` must equal the `vendor/autofde-lab` gitlink. The repository-local
`tests/lock_contracts/test_ecosystem_lock_consistency.py` guard prevents dependency bumps from
leaving the lock behind and prevents a `requires_republish=true` capsule from being represented as
an admitted current release.

The independent `.github/workflows/mfact-certification.yml` court executes this guard on exact
pull-request heads and main pushes before bounded certification. It has VERIFY authority only and
cannot publish a package or promote standing from workflow definition alone.

The owner-catalog counts in `ecosystem.lock.toml` are a dated 2026-08-28 observation receipt. They
are not current ecosystem membership and must be re-censused before being used as a live owner
cardinality projection.

## Promotion falsifier

The release may advance from `BLOCKED` only when all of the following are observed on one exact
subject lineage:

1. the composed image is published successfully;
2. GHCR resolves the immutable digest;
3. a fresh standard consumer pulls that digest;
4. `ggen --version` and marketplace presence pass inside the capsule;
5. a real `ggen sync run` succeeds for the admitted consumer;
6. the receipt binds source, producer, marketplace, image digest, command, exit, and consequence;
7. replay reproduces the same admitted consequence;
8. required architecture crowns are observed before any multi-architecture `ALIVE` claim.

Until then the correct standing is `BLOCKED[GHCR_MANIFEST_UNKNOWN]`, not `ALIVE`.
