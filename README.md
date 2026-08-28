# ggen-ecosystem

Canonical governed composition root for the ggen ecosystem.

This repository owns ecosystem identity, composition, admission, closure, qualification, transport, and release standing. It does not absorb the source identity of `ggen`, `ggen-marketplace`, or independently versioned ecosystem repositories.

## Manufacturing contract

The repository is a first-class GGen consumer:

```text
ggen.toml + ontology.ttl
        +
ggen-marketplace@4c4232515b43d40cef8288c43eacfab2c31ab485
        |
        v
    ggen sync run
        |
        v
.github/workflows/ggen-ecosystem-sync.yml
```

The workflow is a generated consequence. Edit its semantic inputs and regenerate with `ggen sync run`; do not hand-edit the generated workflow.

### Exact producer pins

- GGen release: `v26.8.27`
- GGen source commit behind that tag: `df1e138a64c80e41090cff7c84fb62d77e03b734`
- Linux x86_64 release asset SHA-256: `ab442ced90a9836fd4eb07a5d61eb58293843cd515d864699fc0d0453444a035`
- GGen executable SHA-256 observed during manufacture: `01d0f5e624d12eeda503db4fb4b00618472bd775ee4850c9a2f850651db76680`
- Marketplace commit: `4c4232515b43d40cef8288c43eacfab2c31ab485`
- Marketplace pack: `packs/github-actions-pack`
- Pack content BLAKE3: `1ce72f06a115995a37b9416013d607d4898f3cd707819681a76f663d69c99da8`

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

`.github/workflows/ggen-ecosystem-sync.yml` is both a reusable `workflow_call` target and a manual `workflow_dispatch` rail. It checks out the exact candidate, admits exact producer/pack identities, installs the checksum-pinned GGen release, executes `ggen sync run`, and captures deterministic replay evidence while keeping repository mutation authority outside the workflow (`contents: read` only).

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
