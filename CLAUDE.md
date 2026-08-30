# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`ggen-ecosystem` is the canonical governed **composition root** for the ggen ecosystem. It does not
own the source identity of `ggen`, `ggen-marketplace`, or `autofde-lab` — those are vendored as real
git submodules (`vendor/ggen`, `vendor/ggen-marketplace`, `vendor/autofde-lab`), not URL+SHA references.
This repo owns: ecosystem identity, composition, admission, closure, qualification, transport, and
release standing.

Read `AGENTS.md` first — it is the operating doctrine (authority boundaries, standing vocabulary,
DfCM phases) and takes precedence over generic engineering instinct in this repo.

## Setup

A plain `git clone` does **not** populate the submodules:

```bash
git clone --recurse-submodules <url>       # fresh clone
# or, on an existing plain clone:
make submodules                             # git submodule update --init --recursive
```

## Common commands

Two operator surfaces exist: `Makefile` (minimal contributor wrapper) and `Justfile` (full canonical
surface — run `just --list` for everything). Prefer `just` recipes for anything beyond basic setup.

```bash
make verify        # submodules -> image -> sync -> doctor, in order
just doctor        # pure observation of system state (never repairs) — scripts/doctor.sh
just doctor-json   # same, machine-readable
just alive         # bounded closure toward ALIVE, only safe reversible repairs
just explain       # why current standing exists across all gates
just next          # highest-information lawful next transition
just dod           # live exact-head Definition of Done (scripts/dod_engine.py)
make dod           # print DoD roll-up section only
just chicago       # canonical no-mocks qualification court (12 courts, 59+ assertions) — builds a real Docker image
just certify       # mfact-style certification court (producer pins, artifact authority, receipts, lineage) — ceiling VERIFY, cannot manufacture ALIVE
just certify-test  # adversarial promotion/refusal unit court for certification rules
just falsify       # 25-case adversarial negative-path falsifier suite
just replay        # deterministic replay of prior receipt evidence
just bench         # real wall-clock timing of `ggen sync run --dry-run` (20 runs, min/max/mean/p50/p95)
just stress        # N-way parallel `ggen sync run`, asserts identical graph_hash_hex (default 16-way)
just publication-evidence-test  # 52-case GHCR/OCI publication classification conformance
```

`just chicago` builds a real Docker image (several minutes) — do not run casually mid-swarm; only
the designated build owner should run it during concurrent work (see the warning in `Makefile`'s
`chicago` target).

### Running a single test

Most tests are Chicago-style (no-mocks) Python `unittest` modules or standalone bash scripts under
`tests/`:

```bash
python3 -m unittest tests.test_mfact_certification -v
python3 -m unittest tests.test_ecosystem_alive_cases -v
bash tests/test_container_smoke.sh          # requires a running docker daemon; exits 2 (BLOCKED) if unavailable, never fakes a pass
bash tests/determinism_check.sh
```

## Architecture: SELECT / CONSTRUCT / DO / EVIDENCE

The whole repo is organized around one authority boundary (see README's "Authority boundary"
diagram and `AGENTS.md`'s "Execution" section):

```
SELECT / semantic inputs  -> ontology and profile/admission graphs   (ontology.ttl, ontology/, profiles/)
CONSTRUCT                  -> ggen sync run / deterministic projections (generated/, .github/workflows/*.yml)
EVIDENCE                   -> locks + receipts + replay artifacts     (ggen.lock, ecosystem.lock.toml, receipts/)
DO                         -> external authorized Git/GitHub merge path (never automatic)
```

No graph, planner, hook, generated projection, or workflow ever receives ambient `DO` authority.
`SELECT`, `CONSTRUCT`, and `DO` are distinct steps; only a receipted broker may perform `DO`; CI is
evidence transport, not authority.

### The manufacturing pipeline

```
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

`ggen` is consumed by building a real binary from the vendored `vendor/ggen` submodule into a
composed container (bundled with the real `vendor/ggen-marketplace/packs/`), published to GHCR —
**not** by downloading a release binary tarball. `.github/workflows/ggen-ecosystem-sync.yml` runs
`ggen sync run` inside that pinned container; `.github/workflows/ggen-ecosystem-container.yml`
builds and publishes the container itself. Both generated workflows are a **generated consequence**
of `ontology.ttl` — never hand-edit either; edit the semantic input (`ontology.ttl`) and regenerate
via `ggen sync run`.

`ggen.toml` declares the marketplace pack as a local submodule path
(`vendor/ggen-marketplace/packs/github-actions-pack`), not a `git =`/`version =` fetch. Exact pinned
producer identities (ggen release, source commit, marketplace commit, autofde-lab commit) live in
`ecosystem.lock.toml` and are cross-checked against the vendored gitlinks — do not hand-adjust one
without the other.

### DfCM (Design for Capability Manufacturing) phases

`AGENTS.md` frames all work as: **Preserve -> Fence -> Calculus -> Exclusions -> Falsifier ->
Extension -> Operationalization**. Maximize lawful reversible option capital before any irreversible
selection; a failed edge is topology, not graph failure; bound possibilities by ontology,
capability, authority, cost, evidence, and explicit exclusions. `docs/DFCM.md` and the eight
exhaustive reversible construction candidates (transport / knowledge closure / execution mode) are
the canonical reference — see `README.md`'s "Maximum ecosystem graph" section for the full pipeline
from GitHub owner catalog through admission, profile closure, manufacture, and scoped standing.

### Standing vocabulary — use exactly these terms

`UNKNOWN`, `PARTIAL_ALIVE`, `ALIVE`, `BLOCKED`, `BUILD_BROKEN`, `UNSUPPORTED`, and typed `REFUSED`.
Inspection is not execution; workflow definition is not workflow success; a connector object is not
a mounted tree; a named receipt is not a verified receipt. `scripts/ecosystem_alive.py --explain`
and `docs/CURRENT-RELEASE-STANDING.md` / `docs/STANDING.md` are the sources of truth for current
standing — do not restate a status elsewhere without re-deriving it (drift between restated status
strings has been a real, previously-caught failure mode in this repo).

### Certification vs. manufacturing standing

`certification/mfact.toml` and `certification/artifacts.toml` define an independent mfact-derived
certification court (`scripts/certify_ecosystem.py`, `just certify`). Its authority ceiling is
`VERIFY`: it can bind producer identities, artifact ownership, receipts, replay evidence, Git
lineage, and scoped standing — but it cannot manufacture an `ALIVE` claim or perform `DO`. GGen-
manufactured workflows are projections with zero standing authority regardless of certification
result. `.github/workflows/mfact-certification.yml` is an independent read-only verifier, not a
manufactured workflow projection.

### Key directories

- `ontology.ttl`, `ontology/` — semantic inputs (SELECT layer); `ontology/github-catalog.ttl` encodes
  the maximal public-repo-catalog predicate (`owner=seanchatmangpt AND visibility=public`) — catalog
  membership is observation only, never admission
- `profiles/` — the five semantic profiles: `cloud-session`, `platform-engineering`,
  `process-intelligence`, `autofde`, `everything`
- `admission/`, `certification/`, `contracts/` — admission graphs, mfact certification definitions,
  and formal contracts
- `templates/` — ggen sync templates
- `generated/` — manufactured projections; treat as read-only, repair the source instead
- `receipts/` — machine-readable evidence (bootstrap, benchmark, stress-test); historical receipts
  are admissible evidence for their own recorded head only, never for a newer exact head
- `scripts/` — the operational Python/bash tooling behind every `just`/`make` target
  (`ecosystem_alive.py`, `doctor.sh`, `certify_ecosystem.py`, `dod_engine.py`,
  `chicago_falsifiers.py`, `benchmark.sh`, `stress_test.sh`)
- `tests/` — Chicago-style (no-mocks) test suites; `tests/fixtures/` holds real fixture data (e.g.
  `tests/fixtures/minimal-ggen-project` used by the container smoke test, `tests/fixtures/alive/*.json`
  case files consumed by `test_ecosystem_alive_cases.py`)
- `docs/` — canonical reference docs; `docs/DEFINITION-OF-DONE.md` is the gate matrix (G01-G09 style),
  `docs/ARCHITECTURE.md`, `docs/RECEIPT-SCHEMA.md`, `docs/PROFILES.md`, `docs/GITHUB-CATALOG.md`,
  `docs/MFACT-CERTIFICATION.md` are the deep references for each subsystem above

## Testing discipline

Tests in this repo are Chicago-style (real collaborators, state-based assertions) by explicit repo
convention (`just chicago`, "0 mocks" in the Justfile comment) — this matches the user's global
testing rule. `tests/test_container_smoke.sh` reports `BLOCKED` (exit 2) rather than a fake pass
when Docker is unavailable; preserve that fail-closed pattern in any new test rather than skipping
silently.

## Repository workflow

Per `AGENTS.md`: resolve `main` to an exact SHA, use a purpose branch, never silently move the base,
verify the exact head, and merge only the inspected head when authorized. Preserve typed failures
rather than smoothing them over.
