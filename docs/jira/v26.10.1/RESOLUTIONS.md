# v26.10.1 — RESOLUTIONS (pinned seams; computed by coordinator 2026-10-01, verified against fetched refs)

Do not recompute, do not alter. If your lane's evidence contradicts a value here:
flag `REFUSED_SEAM_CONFLICT` in your lane report and leave the seam unchanged.

## Identity

- milestone tag: `v26.10.1`
- release date: 2026-10-01
- base commit: `dc665a1e93573949040900faa65b46af3a3ea6d9` (= origin/main at dispatch)
- preservation ref: `archive/pre-v26.10.1-dirty-20261001`

## Crown targets (vendor gitlinks → these exact SHAs; coordinator applies at integration)

| vendor | target SHA | target ref evidence |
|---|---|---|
| autofde-lab | `71de04a60db723764fab5afe042b42937b471e0e` | origin HEAD (default branch `master`) |
| beam4pm | `7bad16ab4c20d0eeb90adca1c90a6f3f4d5900dc` | origin/main, describes `v26.9.9-777-g7bad16ab` |
| ggen | `ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e` | origin/main, describes `v26.9.28` |
| ggen-marketplace | `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2` | origin/main, describes `v26.9.30-6-gbf9eccb34` |
| ggen_igniter | `0abed8a35db68c18bba6982b266dd7546c162d1c` | origin/main, describes `v26.9.15-378-g0abed8a` |
| wasm4pm | `a7352d818dbcaa15909833f13ac367dc5950a7a9` | origin/main, describes `v26.9.30-5-ga7352d818` |

Current (pre-bump) gitlink pins live in `HEAD` (=`dc665a1e`) vendor entries; the pre-ff WIP pins
live in `archive/pre-v26.10.1-dirty-20261001:vendor/*`.

## Derived pins

- `[container].tag` → `v26.10.1`, standing `BLOCKED`, `requires_republish = true`
  (image not yet published; precedent: v26.9.25 crown, lock `[container]` section).
- `ontology.ttl` + `ggen-ecosystem-sync.yml` input defaults: tag `v26.9.25` → `v26.10.1`;
  `marketplace_sha` `2c4c4c7e2a4eb33ebe2ad9ab23725af3c476a637` → `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2`.
- `ecosystem.ttl` `dcterms:hasVersion` `"26.8.27"` → `"26.10.1"` (the 2026-10-01 CHANGELOG note
  records this lag as intentional *until the next crown bumps it* — this is that crown).
- `ecosystem.lock.toml` `base_main_sha` → `dc665a1e93573949040900faa65b46af3a3ea6d9`;
  `updated_at` → `2026-10-01T00:00:00Z` (exact stamp = lane wall clock, ISO-8601 Z).
- `[ggen_marketplace].sha` → `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2`.
- `[ggen_igniter].sha` → `0abed8a35db68c18bba6982b266dd7546c162d1c`; `[ggen_igniter].version` =
  observed `mix.exs` `version` at that SHA (read `vendor/ggen_igniter/mix.exs` on the fetched
  ref — `git -C vendor/ggen_igniter show 0abed8a3:mix.exs | grep ^version` — never guessed).
- `[beam4pm].sha`, `[wasm4pm].sha`, autofde section: target SHAs above; `[wasm4pm].version` =
  observed version at target (same method, wasm4pm's version file).

## Delegated decision — L1 only: `[ggen].release`

Facts: ggen repo tag `v26.10.0` exists (`82795cda`) but has **no GitHub release / assets**;
latest asset-bearing release is `v26.9.28` (published 2026-09-29). The lock's `[ggen]` feeds
the consumer-manufacture supply-chain path (`supply-chain-manufacture.yml`), which needs real
release assets + sha256. Lawful options:
(a) `[ggen].release = v26.9.28` + real asset digests (download both release assets, sha256 them
into lane scratch, record; RECOMMENDED — keeps the manufacture path executable), and record the
v26.10.0-no-assets gap as a failed edge in the lane report;
(b) `[ggen].release = v26.10.0` + digests impossible → lock fields degrade to tag-pins +
`BLOCKED[NO_RELEASE_ASSETS]` note (only if (a)'s assets are unfetchable).
Decision + rationale go in the lock (as values/comments per existing style) and the lane report.

## Conflict handoff

`CHANGELOG.md` (L3) and `README.md` (L6) currently carry 3-way conflict markers from the
preserved-WIP re-application (`git apply --3way` over upstream-moved files). Resolve by merging
BOTH intents — origin/main's current content AND the v26.9.25-era standing corrections — then
apply your v26.10.1 changes on top. `git diff archive/pre-v26.10.1-dirty-20261001^ <file>` shows
the WIP intent; the `<<<<<<<` blocks show both sides.

## Integration-owned (coordinator; lanes must not do)

vendor/* gitlinks, `ggen.lock` (`ggen sync`), final `lock_crown_court.py` run, verify ladder,
per-lane atomic commits, tag `v26.10.1`, draft PR.
