# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).
Release identity uses `ecosystem.lock.toml`'s `[ggen].release`/`[container].tag`
`vYY.M.D` convention, e.g. `v26.8.28` — tracking the bundled `ggen` release, not
strict per-commit semver. Several entries below cite the real commit hash(es)
they were derived from so they can be checked with `git show <hash>`; entries
added after the initial `v26.8.28` draft cite PR numbers instead where a squash
merge is the more precise real reference. Pure merge commits are not listed as
separate entries — their content is already covered by the non-merge commits
they bring in.

## [Unreleased]

Nothing yet since the `v26.8.28` tag below.

## [v26.8.28] - 2026-08-29

### Added

- GHCR publication closed end-to-end for
  `ghcr.io/seanchatmangpt/ggen-ecosystem:v26.8.28`: a real `docker push` succeeded
  after refreshing the GitHub OAuth token to `write:packages` scope; a
  network-isolated fresh consumer (`docker run --network none`, `docker pull
  ...@sha256:...`) then independently executed `ggen sync run` against the
  published digest (`8074da6b`).
- `receipts/release-v26.8.28-container.json`: new schema-valid release receipt
  binding the subject commit, `ggen`/marketplace producer commits, container
  digest, and replay-matched consequence digest (`8074da6b`).
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
- Native multi-arch container publish: `build-amd64` (native `ubuntu-24.04`) +
  `build-arm64` (native `ubuntu-24.04-arm`, GitHub's free public-repo arm64
  runner) + `merge-manifest` (`docker buildx imagetools create`), replacing an
  earlier QEMU-emulated single-job attempt that genuinely hit its own 120-minute
  timeout (`ca21ca9d`, `1a2d7b35`).
- Cross-run container build caching: real GHA layer cache (`cache-from`/
  `cache-to: type=gha`) + BuildKit `--mount=type=cache` for cargo's registry,
  sccache, and the target dir — validated locally end to end, including a
  caught-and-reverted near-mistake (a cache mount on `RUSTUP_HOME` would have
  made the installed toolchain invisible to later `RUN` steps) (`27a7b2e7`).
- SBOM + SLSA provenance attestation on both platform builds via
  `docker/build-push-action`'s native `sbom`/`provenance` inputs, #187.
- Keyless container-image signing via cosign + GitHub OIDC (no long-lived
  signing key), #186.
- Trivy container vulnerability scanning with SARIF upload to GitHub code
  scanning, #185.
- `GOVERNANCE.md`, `THIRD-PARTY-LICENSES.md`, this `CHANGELOG.md`, #182–#184.
- Real gymact-admitted, receipted autonomics path (`scripts/
  autonomics_gymact.py`): 4 of 5 `ecosystem_alive.py` safe repair actions now
  run through real admission → execution → SQLite-ledger receipt, gated on live
  `doctor.sh` sensor data.
- Publication evidence falsifier court: 16 new typed falsifier cases (`PUB-035`
  through `PUB-053`) covering the GHCR publication pipeline end to end —
  producer/base-SHA staleness, ownership collisions, registry pull/cache
  integrity, build/push/manifest verification, multi-arch consumer execution,
  and replay/receipt validation.
- Publication evidence court operator surface, `RES-069`, and its evidence case
  envelope, `RES-071`.
- 20-agent Definition-of-Done swarm: 6 real fixes merged (#175–#180), 195/200
  combined falsifier suite.

### Changed

- v26.8.28 producer identities (pinned `ggen` commit, marketplace SHA) projected
  and pinned into `ecosystem.lock.toml` (`ab23c9bb`, `5139d124`).
- Publication and supply-chain evidence courts now execute in CI on the exact PR
  head instead of a stale ref.
- `.github/workflows/ggen-ecosystem-container.yml`'s package visibility issue
  root-caused and fixed: GHCR reports `manifest unknown` (not access-denied) to
  an unauthorized pull of a private package — the composed image was never
  broken, the GHCR package was private. Fixed by making it public; re-verified
  with a genuinely unauthenticated `docker pull` + in-capsule `ggen --version`.

### Fixed

- Two blocked real attempts were recorded with typed standing and exact
  remediation instead of left as `UNKNOWN` or silently retried: the initial GHCR
  push refused with `permission_denied` (OAuth token lacked `write:packages`,
  requires an interactive `gh auth refresh`), and an `act` container run blocked
  by a Colima-specific docker-socket bind-mount defect (`e16feba2`).
- `doctor.sh` false-positive drift flag on independently-authored,
  non-ontology-managed workflows, corrected to informational-only.
- `dod_engine.py` output reconciled with `DEFINITION-OF-DONE.md`, #180.
- Verified-staleness corrected in `REPLAY.md`, #178, and in transport docs
  against the real Dockerfile/workflow/lock, #175.
- Real lint findings closed in `scripts/*.py`, #177.
- Missing `tests/__init__.py` added, restoring test discovery, #176.
- Dijkstra mischaracterization self-corrected: `plan_closure_autofde` is a
  stable sort, not a graph-search planner, after an earlier commit message in
  this same repo's history mischaracterized it as one.
- Publication evidence false-green gap closed, then hardened to enforce exact
  case contract integrity.

### Security

- `PUB-038` unreceipted-`DO` falsifier court, `PUB-039` secret-token-leak
  falsifier court, `PUB-040` docker-config-leak falsifier court.
- SBOM + provenance attestation, cosign keyless signing, Trivy CVE scanning
  (see Added above) — table-stakes container supply-chain security, none of
  which existed before this release.

Real, honest status as of this tag: the image remains **linux/arm64-only** on
the currently *published* digest — the native multi-arch pipeline above is
implemented and locally validated, but publishing the multi-arch manifest for
real still needs one manual step (linking the GHCR package to this repository
under "Manage Actions access," so `GITHUB_TOKEN` can push — confirmed no API
exists for this for either user- or org-owned packages).

[Unreleased]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/v26.8.28...main
[v26.8.28]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/ab23c9bb...v26.8.28
