# ggen-ecosystem

Canonical governed composition root for the ggen ecosystem.

## Five-minute customer path

You do not need to install GGen, clone the marketplace, or edit generated YAML. Add a
caller workflow to your repository that invokes the reusable workflow at this exact
repository/ref, then commit your own `ggen.toml` and ontology instance data:

```yaml
name: Manufacture
on: [pull_request, workflow_dispatch]
jobs:
  ggen:
    uses: seanchatmangpt/ggen-ecosystem/.github/workflows/ggen-ecosystem-sync.yml@main
    with:
      ggen_container_image: ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c
      marketplace_sha: 89adf4c8476f7edc8067fdbb1c256cfbfa22df6a
```

The workflow produces a patch and replay receipt. Treat the result as a candidate
until the exact-head court succeeds; generated files are never hand-edited.

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for a complete starter journey and
[docs/FAILURE-ROUTING.md](docs/FAILURE-ROUTING.md) for typed recovery.

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
- `make doctor` -- runs `scripts/doctor.sh` if present; otherwise prints a placeholder note (no such script exists in this repo yet).
- `make verify` -- chains all of the above in order: `submodules` -> `image` -> `sync` -> `doctor`.

### Exact producer pins

- GGen release: `v26.8.28` (real published GitHub release, verified via `gh release list`/`gh release view`)
- GGen source commit: `c61ee99359c9dbc7b3cb71687976932a3e737ed4` (resolved via `git ls-remote --tags`; matches the `vendor/ggen` submodule pin)
- GGen aarch64-apple-darwin release asset SHA-256 (verified via `gh release download` + `shasum -a 256`, historical — no longer the consumption path): `82123e4dcfcd57d0b07852d0123e52bbaadc99fa076fcaa126855a1c960f9b42`
- Marketplace commit: `89adf4c8476f7edc8067fdbb1c256cfbfa22df6a` (matches the `vendor/ggen-marketplace` submodule pin)
- Marketplace pack: `packs/github-actions-pack` (sourced via local submodule `path =`, not `git =`/`version =`)
- Composed container: `ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c` (immutable release capsule; multi-architecture publication is required for subsequent releases)

## Maximum ecosystem graph

The manufacturing rail above is the proven operational path. The semantic control plane around it is intentionally larger:

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

`.github/workflows/ggen-ecosystem-sync.yml` is both a reusable `workflow_call` target and a manual `workflow_dispatch` rail. It checks out the exact candidate (with submodules), admits exact producer/pack identities, runs its `construct` job **inside** the pinned `ghcr.io/seanchatmangpt/ggen-ecosystem` container, executes `ggen sync run`, and captures deterministic replay evidence while keeping repository mutation authority outside the workflow (`contents: read` only). `.github/workflows/ggen-ecosystem-container.yml` builds and publishes that container from `vendor/ggen` + `vendor/ggen-marketplace` on tag push or manual dispatch.

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

The machine-readable bootstrap receipt is in `receipts/bootstrap-ggen-ecosystem-sync.json`.

## Authority boundary

```text
SELECT / semantic inputs  -> ontology and profile/admission graphs
CONSTRUCT                  -> ggen sync run / deterministic projections
EVIDENCE                   -> locks + receipts + replay artifacts
DO                         -> external authorized Git/GitHub merge path
```

No graph, planner, hook, generated projection, or workflow receives ambient DO authority.
