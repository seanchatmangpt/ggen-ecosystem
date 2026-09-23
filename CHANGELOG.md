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

## [v26.9.22] - 2026-09-23

Release identity follows the vYY.M.D convention (see the format note above).
Commit hashes below are real and checkable with `git show <hash>`.

### Added

- SA2A plan-only court in the composed image, both architectures: the container
  now builds `/opt/sa2a-venv` (pydantic v2, pyshacl, real PyPI wrapt) and the
  image build itself fails if `autofde_lab.sa2a` /
  `autofde_lab.sa2a.admission.pipeline` cannot be imported from the pinned
  `vendor/autofde-lab` gitlink; the canonical publisher runs the same probe as
  a per-arch court step against the just-pushed `-amd64`/`-arm64` images
  (ced8c5af). Previously the probe failed three ways against the shipped
  image: Debian python3-wrapt lacks `wrapt.lru_cache`, pydantic was absent,
  and pyshacl was absent.

### Changed

- Autonomic crown and PragProg TPS run their submodule materialization under
  `GIT_LFS_SKIP_SMUDGE=1` (71e42710, a533e046): the reconcile and candidate
  courts died in LFS smudge (`agrovoc_lod.nt.zip`, "repository exceeded its
  LFS budget") — the `BLOCKED[LFS_BUDGET]` class that also kept PR #348 red.
- `ggen.toml` no longer cites a marketplace SHA in the `[packs]` comment: the
  crown's authorized-path gate forbids ggen.toml edits, so any cited SHA rots
  at the next crown bump. The drift tripwire
  `test_ggen_toml_packs_comment_marketplace_sha_matches_lock` now treats "no
  citation" as the sanctioned state and still fails on a wrong citation
  (71e42710).
- `ggen-ecosystem-sync.yml` workflow_call defaults and their ontology.ttl
  projection bumped from the dead `v26.8.28` container tag to `v26.9.22`, and
  the `marketplace_sha` default from `c779aec2` to the pinned
  `616e93d1e6f9566e4b5eb4e2c3d1400746786e50` (this release).
- `[ggen].release` / `[container].tag`: v26.9.17 → v26.9.22. `[container]`
  stands BLOCKED/requires_republish until the tag build publishes; the digest
  follow-up commit lands with the real digest per release-receipt discipline.

### Fixed

- PR #348 (adopt/engineering-standards-v26.9.21) re-qualified and merged
  (7758dc60) after the LFS guard turned its only red check green.
- Session history landed as repo docs: the 27 v26.9.18 wave-plan tickets +
  v26.9.19 survey restored from the W0 preserve and merged via #367, with
  evidence-checked resolution marks (003→#248, 004→#263, 005→#266; 009 stays
  IN_PROGRESS — #174 was closed stale, not merged).

## [v26.9.17] - 2026-09-17

### Added

- `docs/RFC-GPACK-001-v26.9.17.md`: the **GGEN Semantic Pack Protocol** proposed
  standard, landed verbatim from the operator-supplied draft (2889 lines). Defines
  the GGEN Pack as a portable, content-addressable, ontology-backed semantic
  manufacturing unit binding Identity + Semantics + Dependencies + Admission +
  Projection + Authority + Evidence + Lifecycle, and formalizes the separations the
  current three implementations diverge on: `Query ≠ Gate` (gates are refusal
  falsifiers, queries are render-binding inputs), `RendererIdentity ≠
  FileExtension` (`.tmpl` must not remain the sole renderer authority),
  `Dependency ≠ AmbientProjection` (SEMANTICS/LAW/PROJECTION scope algebra), one
  bootstrap manifest identity contract, and a canonical typed RDF binding model as
  the cross-engine comparison oracle. Also specifies the canonical SHA-256
  PackDigest, target-ownership collision law, `PackAuthority ≤ CONSTRUCT` ceiling,
  portable receipt envelope, typed refusal vocabulary, 15 portable conformance
  courts, the first conformance corpus, and compatibility-preserving migration
  ladders for Rust `ggen`, `ggen_igniter`, and `ggen-marketplace` (legacy profiles
  `GGEN-PACK-RUST-LEGACY-1` / `GGEN-PACK-IGNITER-LEGACY-1` keep existing packs
  valid). Grounded against the exact producer heads this release pins:
  ggen `ad3a7e661`, ggen-marketplace `800b8c6c5`, ggen_igniter `15305cea`.
  The RFC's recommended first implementation artifact (`ggen-pack-spec-pack` +
  first cross-engine portable fixture, Appendix E crown) is explicitly future
  work, not this release.
- `tests/lock_contracts/test_ecosystem_lock_consistency.py::
  test_ggen_toml_packs_comment_marketplace_sha_matches_lock`: permanent tripwire
  for the comment-vs-pin drift class fixed in #248/#263/#266/#267 — any 40-hex
  SHA cited in a `ggen.toml` comment must equal the lock's pinned
  `ggen_marketplace_commit`. Falsified both ways before landing: passes on the
  corrected comment, fires on main's stale comment.
- `docs/jira/v26.9.17/`: milestone session records — the cross-family
  cleanup/merge investigation and additive merge pass (including one correction:
  its log had reported PR #267 as merged, but `7e62e475` is not an ancestor of
  `origin/main`; that fix is superseded by this release's comment correction +
  tripwire), and this release's ticket.

### Changed

- Release identity `v26.9.10` -> `v26.9.17` (`[ggen].release` +
  `[container].tag` in `ecosystem.lock.toml`, this repo's own `vYY.M.D`
  convention). Producer pins are unchanged from the post-v26.9.10 crown
  reconciliations (ggen `ad3a7e661`, ggen-marketplace `800b8c6c5`,
  ggen_igniter `15305cea` — the exact heads the RFC was inspected against), so
  this is a spec-landing + release-identity bump, not a producer re-pin.
- Pushing tag `v26.9.17` triggers `ggen-ecosystem-container.yml`, whose fresh
  build is the path to clearing the standing `[container] standing = BLOCKED /
  requires_republish` state (marketplace pin postdates the v26.9.10-era image).
  Per this repo's release-receipt discipline, `[container]` digest/standing are
  updated in a follow-up commit only after that real build succeeds — never
  fabricated ahead of it.

### Fixed

- `ggen.toml` `[packs]` comment cited stale ggen-marketplace SHA `363b616e`
  while the vendored submodule and lock pin `800b8c6c5` (cosmetic only — the
  `[packs]` entry is a relative `path =` reference, not a SHA pin — but the same
  class has recurred five times; now guarded by the tripwire above).
- Container build unblocked: `vendor/beam4pm` @ `22fa4aac` pinned
  `native/ferroplan` at `4b8ff2ef`, which the ferroplan remote no longer serves
  ("upload-pack: not our ref" after an upstream history rewrite) — every
  `--recursive` checkout died with git exit 128, failing the tag-`v26.9.17`
  container run (35303904365) and the 22:06Z main dispatch before it. Fixed
  upstream in beam4pm PR #74 (gitlink reverted to `29134d7b`, the pin the last
  successful image build ran, verified still directly fetchable; beam4pm's other
  nested pins verified fetchable); this repo advances the pin to merged head
  `fc164d7d`. The `v26.9.17` image is then published via the container
  workflow's `workflow_dispatch` path (`image_tag: v26.9.17`) rather than by
  moving the already-pushed git tag.

## [v26.9.10] - 2026-09-10

### Changed

- `[ggen].release` bumped `v26.8.28` -> `v26.9.10`, matching this
  ecosystem's own `vYY.M.D` release identity (per this file's format
  note, `[ggen].release` mirrors `[container].tag` -- it is the
  ecosystem's own version label, not a literal upstream `ggen` tag name;
  confirmed by inspecting the prior pin: commit `36caa86e`, labeled
  `release = "v26.8.28"`, is actually only reachable from real upstream
  tags `v26.9.8`/`v26.9.9`). `[ggen].commit_sha` is the field that pins
  the real upstream commit: bumped `36caa86e` -> `83a02070`, the real
  latest upstream `ggen` release as of this bump (`v26.9.9`, 2026-09-08;
  no real upstream `v26.9.10` tag exists). `linux_x86_64_asset_sha256`
  and `aarch64_apple_darwin_asset_sha256` are the real published sidecar
  checksums from that `v26.9.9` GitHub Release (cross-verified locally
  against a real downloaded tarball, not copied blind);
  `observed_executable_sha256` is the digest of the extracted binary
  itself, actually run (`ggen --version` -> `26.9.9`), closing the
  `linux_x86_64_asset_sha256`/`observed_executable_sha256`
  `UNKNOWN-TODO` gap this file has carried since before `v26.8.28`.
- `vendor/ggen-marketplace` (`[ggen_marketplace].sha`,
  `[submodules].ggen_marketplace_commit`, `[pragprog_tps].marketplace_sha`,
  and `ggen.toml`'s `[packs]` comment) bumped `1bf36244` -> `b82ee3ee`,
  picking up three real fixes on `ggen-marketplace` main: PR #426 (18
  triaged remote branches integrated, real merge-conflict resolution, one
  broken stub pack dropped), PR #427 (real `ggen sync run` qualification
  found and fixed concrete defects in `github-actions-pack` -- the exact
  pack this repo's own `ggen.toml` composes --, `frontier-release-factory-
  pack`, `planning-federation-pack`, and `ash-extension-core-pack`), and
  PR #429 (`local_dispatch.sh.tmpl` crashed `[FM-TPL-017]` on this exact
  repo's own zero-`LocalExecutionProfile` consumer graph -- found
  manufacturing this release, fixed upstream rather than patched locally;
  see that repo's own CHANGELOG-equivalent commit messages for detail). No
  other vendor submodule (`autofde-lab`, `ggen_igniter`, `beam4pm`,
  `wasm4pm`) was touched in this release -- out of scope for a ggen-core +
  marketplace bump.
- `vendor/ggen` submodule gitlink advanced to the new pinned commit
  (`83a02070`) to match `[ggen].commit_sha`.

### Added

- GHCR publication closed end-to-end for
  `ghcr.io/seanchatmangpt/ggen-ecosystem:v26.9.10`: pushing the `v26.9.10`
  tag triggered `ggen-ecosystem-container.yml` for real (run
  `34520804764`), building and pushing both `linux/amd64` and
  `linux/arm64` images and merging them into one multi-arch manifest,
  digest `sha256:c98bd277...`. Independently re-pulled
  (`docker pull ghcr.io/seanchatmangpt/ggen-ecosystem:v26.9.10`) and
  confirmed the identical digest, then ran a network-isolated consumer
  (`docker run --rm --network none ... ggen --version`) that printed
  `ggen 26.9.9` -- the exact pinned upstream release, proven inside the
  published image, not assumed from the build log. `[container]` in
  `ecosystem.lock.toml` updated to this tag/digest/run in the same
  release, rather than left pointing at the stale `v26.8.28` receipt
  (closing the honest `CONTAINER_RELEASE_TAG_DRIFT` refusal
  `certify_ecosystem.py` correctly raised on this PR before the real
  build ran).

### Fixed

- `ecosystem.lock.toml`'s `[container]` block corrected a stale
  `standing = "BLOCKED"` (with `requires_republish = true`, pinned to a
  historical `observed_failure_run`) even though
  `ggen-ecosystem-container.yml` has been green on `main` continuously
  since run `33926356178` at `base_main_sha`. Flipped standing to `ALIVE`,
  cleared `requires_republish`, and preserved the historical failure run
  alongside new `observed_success_run`/`observed_success_at`/
  `observed_success_head_sha` fields rather than deleting the prior
  observation, #268.
- `scripts/certify_ecosystem.py`'s `validate_release_receipt()` stopped
  hard-failing `mfact-certification.yml` on every run by comparing a
  versioned, point-in-time release receipt against the ever-moving
  current `ecosystem.lock.toml`. The identity check now only escalates to
  a hard error when the receipt's subject commit is the current git HEAD;
  elsewhere the drift folds into the existing historical-evidence
  discount already documented in `certification/mfact.toml`'s
  `[subject]` policy, #263.
- `tps/run.sh` (PragProg TPS) stopped hardcoding
  `EXPECTED_MARKETPLACE_SHA` as a literal constant — a no-dual-bookkeeping
  duplicate of `ecosystem.lock.toml`'s `[pragprog_tps].marketplace_sha`
  that had gone stale after a submodule reconciliation advanced the lock
  without updating the script's own copy, causing a live
  `REFUSED[PRAGPROG_PACK_DRIFT]` failure. Now reads the value from the
  lock file at runtime instead, #266.
- `ggen.toml`'s `[packs]` section comment cited a stale
  `vendor/ggen-marketplace` pin (`89adf4c8...`, dated 2026-08-28); updated
  to the real, currently-vendored `427366d1f...`, matching both
  `ecosystem.lock.toml` and the actual submodule HEAD. Cosmetic only —
  the real `[packs]` dependency is a relative `path =` reference, not a
  SHA pin — but the same historical-drift comment-vs-pin pattern as
  #248/#263/#266, #267.

### Changed (carried from Unreleased)

- `vendor/autofde-lab` submodule pin synced from a 9-day-stale
  `autofde_lab_commit` to `autofde-lab`'s real `origin/master` tip;
  `vendor/beam4pm` bumped to its real post-fix HEAD (`beam4pm#47` merged,
  fixing a `.gitmodules` bug that was blocking Qualify checks on this PR)
  and both `[beam4pm].sha` and the separate `[submodules].beam4pm_commit`
  field brought into agreement, #248.

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

[Unreleased]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/v26.9.10...main
[v26.9.10]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/v26.8.28...v26.9.10
[v26.8.28]: https://github.com/seanchatmangpt/ggen-ecosystem/compare/ab23c9bb...v26.8.28
