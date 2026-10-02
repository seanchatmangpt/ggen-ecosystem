# Current release standing

This page is the canonical current release-standing correction for the composed `ggen-ecosystem` capsule. Older Definition-of-Done rows remain historical execution evidence and must not be interpreted as fresh availability claims after the exact subject changes.

## Exact admitted subject

- repository: `seanchatmangpt/ggen-ecosystem`
- reconciliation ancestor: `dc665a1e93573949040900faa65b46af3a3ea6d9`
- ggen source: `ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e` (tag `v26.9.28` — the latest asset-bearing ggen release; tag `v26.10.0` exists upstream with a zero-asset release object)
- marketplace source: `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2` (describes `v26.9.30-6`)
- ggen_igniter source: `0abed8a35db68c18bba6982b266dd7546c162d1c` (version 26.9.30)
- autofde-lab gitlink: `71de04a60db723764fab5afe042b42937b471e0e`

Updated 2026-10-01 from ecosystem.lock.toml @ release/v26.10.1.

The current repository head must be resolved at verification time; the ancestor above records the reconciliation lineage, not a claim that future heads inherit execution evidence automatically.

## Capsule standing

`ALIVE` as of the v26.10.1 publish (2026-10-01): the lock's `[container]` section
records the composed multi-arch image for tag `v26.10.1` (`sha256:cf0612ae22425c94731dc7bc43ea857a02ab30910a4f91a80e9eb902e7f06004`), built by
container run `36924410651` @ head `e4be6fee4edecb2075a3a5a6863058051ecbed82`
(2026-10-01T21:16:44Z), with the digest independently re-fetched anonymously from
the public GHCR index (`docker buildx imagetools inspect`, no local credentials),The image was then anonymously pulled and `ggen --version` executed in-container (`ggen 26.9.28`, matching `[ggen].upstream_release`).
The prior `sha256:6605878ee50f897947560445f655602e9f4471dcaeb4c493a0ce55dbec4bec13`
digest remains historical evidence of the v26.9.22-era image only (observed run
`35833887166`, 2026-09-23). See `ecosystem.lock.toml [container]`.

History: the v26.9.25 crown (2026-09-26) and the v26.9.29 crown (2026-09-29) each
recorded this same `BLOCKED[AWAITING_PUBLISH]` state against the same v26.9.22-era
digest and were superseded without a publish. The prior `ALIVE` verdicts below held
for that v26.9.22-era digest.

Root cause of the historical `BLOCKED[GHCR_MANIFEST_UNKNOWN]` (2026-08-29): the
`ghcr.io/seanchatmangpt/ggen-ecosystem` package was **private**. GHCR reports `manifest unknown`
to an unauthorized puller of a private package rather than an access-denied error, which is what
GitHub-hosted Actions run `33238309149` actually hit -- the digest itself was never broken. Fixed
by changing the package's visibility to public via the GitHub web UI (no API exists for this, for
either user- or org-owned packages -- confirmed against GitHub's own REST documentation before
concluding that).

Historical (2026-08-29, ALIVE era): re-verified for real against the then-recorded digest,
`ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c`,
with `docker logout ghcr.io` first (confirmed no credentials) and the local image cache fully
removed before pulling: real layer downloads (not a cache hit), then a real in-capsule
`ggen --version` -> `ggen 26.8.28`. No rebuild or republish was needed then.

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
