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

`ALIVE`

Root cause of the historical `BLOCKED[GHCR_MANIFEST_UNKNOWN]` (2026-08-29): the
`ghcr.io/seanchatmangpt/ggen-ecosystem` package was **private**. GHCR reports `manifest unknown`
to an unauthorized puller of a private package rather than an access-denied error, which is what
GitHub-hosted Actions run `33238309149` actually hit -- the digest itself was never broken. Fixed
by changing the package's visibility to public via the GitHub web UI (no API exists for this, for
either user- or org-owned packages -- confirmed against GitHub's own REST documentation before
concluding that).

Re-verified for real against the **same** digest,
`ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c`,
with `docker logout ghcr.io` first (confirmed no credentials) and the local image cache fully
removed before pulling: real layer downloads (not a cache hit), then a real in-capsule
`ggen --version` -> `ggen 26.8.28`. No rebuild or republish was needed.

GitHub issue `#146` is closed with this evidence attached.

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

## Promotion falsifier (satisfied 2026-08-29)

1. the composed image is published successfully -- yes, `sha256:b9e170233fe1...`.
2. GHCR resolves the immutable digest -- yes, `gh api /user/packages/container/ggen-ecosystem`
   reports `"visibility": "public"`.
3. a fresh standard consumer pulls that digest -- yes, unauthenticated `docker pull` by digest,
   fresh layer downloads, verified this session.
4. `ggen --version` and marketplace presence pass inside the capsule -- yes, `ggen 26.8.28`
   confirmed in the same unauthenticated pull.
5. a real `ggen sync run` succeeds for the admitted consumer -- yes, see
   `receipts/release-v26.8.28-container.json`.
6. the receipt binds source, producer, marketplace, image digest, command, exit, and consequence --
   yes, same receipt file, schema-validated by `scripts/verify-receipt.sh`.
7. replay reproduces the same admitted consequence -- yes, `tests/replay_check.sh` real run:
   `== REPLAY MATCH: consequence digest identical ==`.
8. required architecture crowns are observed before any multi-architecture `ALIVE` claim -- **not
   yet**: the published image remains linux/arm64-only, not verified on a standard amd64
   GitHub-hosted runner. This is the one open item; `docs/DEFINITION-OF-DONE.md` PR-009 tracks it
   as the remaining honest gap, not silently dropped.
