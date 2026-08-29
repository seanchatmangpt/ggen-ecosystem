# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
This repository has no `git tag` objects yet (`git tag -l` is empty) — release
identity is instead tracked in `ecosystem.lock.toml` (`[ggen].release`,
`[container].tag`) using a `vYY.M.D` identifier, e.g. `v26.8.28`. Each entry below
cites the real commit hash(es) it was derived from so it can be checked with
`git show <hash>`. Pure merge commits (`bc8c39b2`, `2eb1ede5`, `5380352b`,
`e2c1f081`) are not listed as separate entries — their content is already covered
by the non-merge commits they bring in.

## [Unreleased]

### Added

- Publication evidence falsifier court: 16 new typed falsifier cases covering the
  GHCR publication pipeline (producer/base-SHA staleness, ownership collisions,
  registry pull/cache integrity, build/push/manifest verification, multi-arch
  consumer execution, and replay/receipt validation). Security-classified cases
  `PUB-038`–`PUB-040` are listed under Security below.
  - `PUB-035` stale-producer-sha (`329e8dde`)
  - `PUB-036` stale-base-sha (`acf098de`)
  - `PUB-037` ownership-collision (`9fd6f16f`)
  - `PUB-041` pull-unknown-manifest (`efda2068`)
  - `PUB-042` pull-denied-private (`d871b4d6`)
  - `PUB-043` cache-digest-mismatch (`15e71e8e`)
  - `PUB-044` cache-hit-no-registry-evidence (`d3fc7d61`)
  - `PUB-045` build-success-no-push (`8d6be992`)
  - `PUB-046` push-success-no-digest (`ce38c9da`)
  - `PUB-047` manifest-success-no-consumer (`b6f247c1`)
  - `PUB-048` consumer-amd-fails (`07a9f8ef`)
  - `PUB-049` consumer-arm-fails (`888da65c`)
  - `PUB-050` replay-mismatch (`cdb10cd5`)
  - `PUB-051` receipt-invalid (`8a1e2207`)
  - `PUB-052` complete-index-no-replay (`f3217b3a`)
  - `PUB-053` complete-multiarch-crown (`986ea440`)
- Publication evidence court operator surface, `RES-069` (`73c40d7d`), and its
  evidence case envelope, `RES-071` (`64f2c242`).
- 20-agent Definition-of-Done swarm receipt recorded: 195/200 combined suite
  (`4c3ddeb9`).
- Real doctor snapshot captured post publication-evidence-court merge (`fa462660`).
- 4th autonomics safe action: fresh-consumer verify, #179 (`5c43be72`).

### Changed

- Cross-run container build caching: real GHA layer cache + BuildKit mounts
  (`27a7b2e7`).
- Publication and supply-chain evidence courts now execute in CI on the exact PR
  head instead of a stale ref (`bff63ade`, `c061b88a`).
- Typed registry recovery routed for publication docs, `RES-037` (`0240fb07`).

### Fixed

- `dod_engine.py` output reconciled with `DEFINITION-OF-DONE.md`, #180
  (`1888350a`).
- Verified-staleness corrected in `REPLAY.md`, #178 (`69e0e9a2`), and in transport
  docs against the real Dockerfile/workflow/lock, #175 (`09a7436d`).
- Real lint findings closed in `scripts/*.py`, #177 (`7862a3e5`).
- Missing `tests/__init__.py` added, restoring test discovery, #176 (`9e5edf92`).
- Dijkstra mischaracterization corrected in docs/tests; 2 stale fingerprints fixed
  (`254a03f4`).
- Publication evidence false-green gap closed (`463cf5e4`), then merged and
  hardened to enforce exact 52-case contract integrity (`aa4e15c6`).

### Security

- `PUB-038` unreceipted-`DO` falsifier court: verifies no unreceipted
  mutation-authority action escapes detection in the publication pipeline
  (`f2333b58`).
- `PUB-039` secret-token-leak falsifier court (`4f5f9cef`).
- `PUB-040` docker-config-leak falsifier court (`cecc3ae4`).

## [v26.8.28] - 2026-08-28

### Added

- GHCR publication closed end-to-end for
  `ghcr.io/seanchatmangpt/ggen-ecosystem:v26.8.28`: a real `docker push` succeeded
  after refreshing the GitHub OAuth token to `write:packages` scope; a
  network-isolated fresh consumer (`docker run --network none`, `docker pull
  ...@sha256:...`) then independently executed `ggen sync run` against the
  published digest (`8074da6b`).
- `receipts/release-v26.8.28-container.json`: new schema-valid release receipt
  binding the subject commit, `ggen`/marketplace producer commits, container
  digest, and replay-matched consequence digest; standing recorded as
  `PARTIAL_ALIVE` (held back from `ALIVE` because the published image was
  linux/arm64-only, not yet multi-arch verified) (`8074da6b`).
- `tests/replay_check.sh` run for real against the release commit's own
  git-worktree checkout; two real script defects found and fixed along the way
  (stdout+stderr previously conflated into the consequence digest; hardcoded
  `/tmp` paths incompatible with Colima) — final run: REPLAY MATCH (`8074da6b`).
- `act workflow_dispatch -j construct` simulation run against the composed
  container; found and fixed two real production defects at their source — the
  `ggen-marketplace` workflow template was missing `shell: bash`
  (seanchatmangpt/ggen-marketplace#392) and the runtime image was missing `bash`
  — then regenerated `.github/workflows/ggen-ecosystem-sync.yml` via a real
  `ggen sync run` (`8074da6b`).

### Changed

- v26.8.28 producer identities (pinned `ggen` commit, marketplace SHA) projected
  and pinned into `ecosystem.lock.toml` (`ab23c9bb`, `5139d124`).

### Fixed

- Two blocked real attempts were recorded with typed standing and exact
  remediation instead of left as `UNKNOWN` or silently retried: the initial GHCR
  push refused with `permission_denied` (OAuth token lacked `write:packages`,
  requires an interactive `gh auth refresh`), and an `act` container run blocked
  by a Colima-specific docker-socket bind-mount defect (`e16feba2`).

### Security

- No security-classified change in this release beyond the falsifier-court work
  listed under [Unreleased].

> **Known limitation as of this writing (not a v26.8.28-dated commit):** per the
> current `ecosystem.lock.toml`, a later hosted-run replay (Actions run
> `33238309149`) observed the published `v26.8.28` digest returning `manifest
> unknown` on job-container pull. `[container].standing` is currently `BLOCKED`
> with `requires_republish = true`. Noted here so this entry does not overclaim
> present-day pull availability of the `v26.8.28` image.

[Unreleased]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/8074da6b...main
[v26.8.28]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/ab23c9bb...8074da6b
