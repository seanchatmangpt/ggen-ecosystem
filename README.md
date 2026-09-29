# ggen-ecosystem

[![GGen Ecosystem Sync](https://github.com/seanchatmangpt/ggen-ecosystem/actions/workflows/ggen-ecosystem-sync.yml/badge.svg)](https://github.com/seanchatmangpt/ggen-ecosystem/actions/workflows/ggen-ecosystem-sync.yml)
[![Container Build & Publish](https://github.com/seanchatmangpt/ggen-ecosystem/actions/workflows/ggen-ecosystem-container.yml/badge.svg)](https://github.com/seanchatmangpt/ggen-ecosystem/actions/workflows/ggen-ecosystem-container.yml)
[![MFact Certification](https://github.com/seanchatmangpt/ggen-ecosystem/actions/workflows/mfact-certification.yml/badge.svg)](https://github.com/seanchatmangpt/ggen-ecosystem/actions/workflows/mfact-certification.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Canonical governed composition root for the ggen ecosystem.

> **Current release standing:** `BLOCKED[REQUIRES_REPUBLISH]` for ecosystem `v26.9.29`. The producer identities are admitted below, but the composed `v26.9.29` GHCR image has not yet been published and independently re-pulled/replayed. Historical container digests remain evidence for their own subjects only; they do not establish standing for this release. See [docs/DEFINITION-OF-DONE.md](docs/DEFINITION-OF-DONE.md) for the full gate matrix.

This repository owns ecosystem identity, composition, admission, closure, qualification, transport, and release standing. It does not absorb the source identity of `ggen`, `ggen-marketplace`, or independently versioned ecosystem repositories. `ggen` and `ggen-marketplace` are vendored as real git submodules (`vendor/ggen`, `vendor/ggen-marketplace`) rather than referenced only by URL+pinned-SHA in TOML.

## Manufacturing contract

The repository is a first-class GGen consumer. `ggen` itself is consumed by building it from the real `vendor/ggen` submodule into a composed container (bundled with the real `vendor/ggen-marketplace/packs/`), published to GHCR — not by downloading a release binary tarball:

```text
vendor/ggen (submodule)        vendor/ggen-marketplace (submodule)
        |                              |
        v                              v
      Dockerfile  ------------------->  ghcr.io/seanchatmangpt/ggen-ecosystem:<tag>
                                              |
ggen.toml + ontology.ttl                     |
        |                                    v
        +----------------------->  ggen sync run  (runs INSIDE that container)
                                              |
                                              v
                        .github/workflows/ggen-ecosystem-sync.yml
                        .github/workflows/ggen-ecosystem-container.yml
```

Both generated workflows are a generated consequence of `ontology.ttl`. Edit its semantic inputs and regenerate with `ggen sync run`; do not hand-edit either generated workflow. A reusable composite Action (`use-ggen-ecosystem`, in `ggen-marketplace/packs/github-actions-pack/examples/consume-github-actions-pack/`) lets other repos run `ggen sync run` inside the same pinned container without a curl/binary step of their own.

## Local development

This repo vendors `ggen` and `ggen-marketplace` as real git submodules. A plain `git clone` does **not** populate them -- clone with `git clone --recurse-submodules <url>` to get everything in one step, or if you already have a plain clone, run `git submodule update --init --recursive` (also exposed as `make submodules`) before doing anything else.

A `Makefile` at the repo root wraps the common contributor workflows:

- `make submodules` -- `git submodule update --init --recursive`; populates/updates `vendor/ggen` and `vendor/ggen-marketplace`.
- `make image` -- `docker build -t ggen-ecosystem:local .`; builds the composed container from the Dockerfile and the vendored submodules.
- `make sync` -- removes any stale `ggen.lock`, then runs `ggen sync run --dry-run` followed by a real `ggen sync run` against `ontology.ttl`/`ggen.toml`.
- `make doctor` -- runs `scripts/doctor.sh` (11 real checks, no mocks; JSON via `--json`).
- `make verify` -- chains all of the above in order: `submodules` -> `image` -> `sync` -> `doctor`.

A `Justfile` provides the fuller canonical operator surface (`just --list` for all recipes):

- `just chicago` -- the real, no-mocks container smoke test (`tests/test_container_smoke.sh`).
- `just alive` / `just doctor` / `just dod` / `just replay` / `just falsify` -- the closed loop:
  observe -> diagnose -> plan -> repair -> verify -> receipt -> standing.
- `just bench` -- real wall-clock timing of `ggen sync run --dry-run` (20 runs, min/max/mean/p50/p95).
  Latest measured result: p50 96ms, p95 203ms (`receipts/benchmark-sync-dryrun-20260829.json`).
- `just stress` -- real concurrency stress test: N parallel `ggen sync run` processes must all exit
  0 and report the identical `graph_hash_hex`. Verified PASS at 16-way and 64-way parallelism
  (`receipts/stress-test-64way-20260829.json`).

### Exact producer pins

The integration crown and published-release identities are intentionally separate.

- Ecosystem release: `v26.9.29` (container publication still pending).
- GGen published release: `v26.9.28` at
  `ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e` (also the current
  `vendor/ggen` gitlink).
- GGen Linux x86_64 release archive SHA-256:
  `47316dd090d52d3fc7f1ee8185b8fab09e4a69f1a6fd1cf8e083781e192383e6`.
  Release-run build-output SHA-256 for `target/release/ggen`:
  `c44f9c5632de1bf6c7cf926a5cbbd88303c681f1bb976f2e90ef4b3122ae44a6`
  (run `36508964375`, reports `ggen 26.9.28`).
- Marketplace published release: `v26.9.29` at
  `637b561cc6384fc9ac0e4282d048cc7624256258`; rolling
  `vendor/ggen-marketplace` crown:
  `20ac5c935e46b7f0ff1336e7876e7730c935ebde`.
- AutoFDE Lab rolling crown:
  `d42a5af94481a3128bf3e35d5f2a0a9a70f22e41`.
- GGen Igniter rolling crown:
  `4c5eed22252203980060dbc757c447823179253f`, source version `26.9.29`;
  latest observed published GitHub Release remains `v26.8.27`.
- Beam4PM rolling crown:
  `34ce4a23d0c59edab2391f149413bc5fb1e375c3`, source version `26.9.28`;
  no matching `v26.9.28` tag was observed at this release cut.
- WASM4PM rolling crown:
  `2ec870ef6f2411beab238f56859c3ca438455c1c`, source version `26.9.28`;
  latest observed published GitHub Release remains `v26.9.24`.
- Marketplace pack: `packs/github-actions-pack` (sourced via local submodule
  `path =`, not `git =`/`version =`).
- The digest currently retained in `ecosystem.lock.toml [container]` is
  historical evidence only until the `v26.9.29` image is published and
  independently admitted.

## Maximum ecosystem graph

The manufacturing rail above is the proven operational path when its exact capsule identity is admitted. The semantic control plane around it is intentionally larger:

```text
complete public GitHub owner catalog
        -> observed/candidate repository graph
        -> admission + privacy fence
        -> capability/profile closure
        -> DfCM reversible design space
        -> deterministic manufacture
        -> BRCE-bounded DO
        -> receipt + replay
        -> scoped standing
```

The maximal repository scope is **every public repository owned by `seanchatmangpt`**, represented canonically by the predicate `owner=seanchatmangpt AND visibility=public` in `ontology/github-catalog.ttl`. The enumerated repository-census shards are a high-signal materialized subset for initial profile reasoning; they are not the boundary of the `everything` profile.

Catalog membership is observation, not admission. It grants no dependency edge, compatibility claim, execution status, or mutation authority by itself. Private repository identities are not projected into this public repository.

Five semantic profiles are defined: `cloud-session`, `platform-engineering`, `process-intelligence`, `autofde`, and `everything`. The source DfCM bootstrap space preserves eight exhaustive reversible construction candidates across transport, knowledge closure, and execution mode.

## GitHub-native cloud bootstrap

`.github/workflows/ggen-ecosystem-sync.yml` is both a reusable `workflow_call` target and a manual `workflow_dispatch` rail. It checks out the exact candidate (with submodules), admits exact producer/pack identities, runs its `construct` job **inside** the pinned `ghcr.io/seanchatmangpt/ggen-ecosystem` container, executes `ggen sync run`, and captures deterministic replay evidence while keeping repository mutation authority outside the workflow (`contents: read` only). `.github/workflows/ggen-ecosystem-container.yml` builds and publishes that container from `vendor/ggen` + `vendor/ggen-marketplace` on tag push or manual dispatch. The workflow definition is present, but the current capsule must be republished before this path can regain `ALIVE` standing.

## Provenance

The initial workflow bytes were manufactured by the real GGen release through GitHub Actions, not authored directly:

- GGen branch head: `dcd363b5bcc0ba526bb6ce5e6bc4ea5db0a1a716`
- GitHub self-test run: `33150915638`
- job: `98782446151`
- evidence artifact: `9677675572`
- evidence artifact digest: `sha256:0455db2b422807c78e64324a009cd7b2d393538be72eef543512df05ab6e80b5`
- generated workflow SHA-256: `e03c5da8306d7b7073787c5d4172cfecafd296a4283adb05272ae465b392308e`
- generated graph hash: `27500c768263ba41ad5343a08a8d521c1f12c06e74d7089c4650a298d0b02ad2`
- `ggen sync run` exit: `0`
- independent YAML parse: `PASS`

The machine-readable bootstrap receipt is in `receipts/bootstrap-ggen-ecosystem-sync.json`. It is historical evidence; it does not certify the current repository head or current GHCR availability.

## Authority boundary

```text
SELECT / semantic inputs  -> ontology and profile/admission graphs
CONSTRUCT                  -> ggen sync run / deterministic projections
EVIDENCE                   -> locks + receipts + replay artifacts
DO                         -> external authorized Git/GitHub merge path
```

No graph, planner, hook, generated projection, or workflow receives ambient DO authority.
