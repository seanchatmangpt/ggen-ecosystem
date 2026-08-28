# GGen Ecosystem v26.8.28 — PRD / ARD

**Release:** v26.8.28
**Program:** GGen Ecosystem
**Release Theme:** Portable GitHub-Native Software Manufacturing
**Target Standing:** `ALIVE`
**Strategic Horizon:** Vision 2030 — Autonomic Software Manufacturing
**Primary Repository:** `ggen-ecosystem`
**Producer Repositories:** `ggen`, `ggen-marketplace`
**Primary Consumer Surface:** GitHub Actions
**Canonical Manufacture Command:** `ggen sync run`

This document is the release Product Requirements Document / Architecture Requirements
Document for v26.8.28. It separates *what* the release must deliver (Part I) from *how* it must
be built (Part II), and makes the fresh independent consumer the crown acceptance boundary. The
executable Definition of Done that operationalizes every `PR-*`/architecture item below lives in
[`DEFINITION-OF-DONE.md`](DEFINITION-OF-DONE.md) — the two documents share the same completion
calculus; this file states requirements, that one states executed evidence.

## See Also

- [`DEFINITION-OF-DONE.md`](DEFINITION-OF-DONE.md) — executable acceptance matrix for every
  `PR-*` requirement below
- `../scripts/doctor.sh` — typed-standing diagnostic surface (PR-013)
- `../tests/test_container_smoke.sh` — Chicago-style real-boundary qualification (PR-015)
- `../Makefile` — DX entry points composing the canonical operations (UX-001)
- `../STANDING.md` (`../docs/STANDING.md`) — the standing vocabulary this document binds to

---

# Part I — Product Requirements Document

## 1. Product Definition

GGen Ecosystem v26.8.28 shall establish a **portable, immutable, independently consumable
software-manufacturing environment** composed from the exact GGen implementation and exact GGen
Marketplace knowledge.

A consumer repository shall be able to reference the ecosystem and execute deterministic
manufacture without independently:

- downloading a GGen release binary,
- compiling GGen,
- cloning or resolving GGen Marketplace,
- knowing GGen's Rust workspace topology,
- knowing where marketplace packs reside,
- reproducing bootstrap tooling,
- maintaining bespoke GGen installation logic.

The release product is therefore not a Docker image by itself. The product is the complete
executable relationship:

```text
Consumer Intent + Exact Ecosystem Identity --mu--> Verified Artifact + Receipt
```

The container, reusable GitHub Action, submodules, workflows, doctor, Chicago tests, Definition
of Done, receipts, and replay facilities exist to make that relationship executable.

## 2. Problem Statement

Before v26.8.28, the GitHub-native consumption path required repositories or workflows to obtain
GGen separately, including a generated workflow path that downloaded a release tarball with
`curl` and verified it using `sha256sum`. GGen did not provide the required combined execution
unit containing both the generator and marketplace packs.

That architecture creates several forms of manufacturing knowledge leakage. A consumer must
potentially know installation, version, marketplace, toolchain, and CI concerns that are not
domain concerns — they belong to the ecosystem. v26.8.28 must drive that leakage to zero for all
derivable GGen bootstrap concerns.

## 3. Product Thesis

If GGen source identity, marketplace knowledge, execution dependencies, validation mechanisms,
and provenance are composed into one immutable ecosystem identity, then a clean consumer can
manufacture itself without reconstructing the GGen environment.

The release succeeds only if this hypothesis is observed against a real consumer. Construction is
insufficient. A successful Docker build is insufficient. A successful generated workflow is
insufficient. A successful marketplace render is insufficient. `ALIVE` is reached only when the
composed environment is actually built and pushed and a real consumer pulls and executes it
end-to-end.

## 4. Users

- **Primary — Consumer Repository**: declares project semantics, selects an exact ecosystem
  identity, invokes manufacture, receives artifacts + evidence. Never operates the GGen toolchain
  directly.
- **Secondary — Ecosystem Maintainer**: maintains composition, exact producer identities,
  marketplace compatibility, execution capsule, validation policy, release standing.
- **Secondary — Marketplace Maintainer**: maintains reusable executable knowledge, including
  GitHub-native consumption structures generated (not hand-authored) for consumers.
- **Machine Consumer**: GitHub Actions, local `act`, cloud development sessions, autonomous
  workstations, future build plants — all must consume the same ecosystem identity through a
  deterministic, machine-addressable interface.

## 5. Product Goal

```text
Fresh Consumer Repository + Exact Ecosystem Reference
  -> Clean GitHub Runner
  -> Pull immutable GGen ecosystem
  -> ggen sync run
  -> Generated Consequence
  -> Qualification
  -> Receipt
  -> ALIVE
```

The consumer shall require no prior GGen installation.

## 6. Product Non-Goals

v26.8.28 is not intended to complete Vision 2030, migrate every consumer repository, implement
all industry closures, create a new general-purpose orchestration platform, rewrite GGen or
GGen Marketplace, replace GitHub, introduce arbitrary new pack families, build generalized
knowledge-hook infrastructure, optimize every GGen performance characteristic, or solve every
existing ecosystem backlog item. Work outside the portable-manufacturing crown path is excluded
unless necessary to restore closure.

## 7. Current Observed Baseline

`ggen-ecosystem` is the composition root rather than a conventional application repository — the
repository is primarily semantic/configuration material rather than application source. The
chosen architecture binds real `ggen` and `ggen-marketplace` repositories as git submodules and
builds a composed container containing both the GGen executable and marketplace packs. The
marketplace-side reusable Action executes `ggen sync run` inside that composed environment rather
than downloading a binary into the consumer runner. Real local work has identified runtime
dependencies such as `git` and `python3` needed by the admission/evidence steps inside the
composed container.

These facts define the implementation baseline. They do **not** by themselves establish release
`ALIVE`.

## 8. Product Requirements

Each requirement's acceptance evidence is tracked in `DEFINITION-OF-DONE.md`'s acceptance matrix,
identified by the same `PR-###` id.

- **PR-001 — Exact Ecosystem Identity.** One exact v26.8.28 composition `(G, M, C, V, P)`: exact
  GGen commit, exact marketplace commit, exact capsule digest, validation identity, admission
  policy. No release-critical producer identity is `UNKNOWN`, fabricated, nonexistent, or
  floating.
- **PR-002 — Real Source Composition.** `ggen` and `ggen-marketplace` incorporated as genuine
  independently versioned source dependencies via gitlinks/submodules, preserving their
  repository identities rather than copying source. `git submodule status` resolves both at the
  admitted commits from a clean checkout.
- **PR-003 — No Binary-Download Consumer Path.** The canonical generated consumer workflow
  contains no GGen release `curl`/tarball installation sequence.
- **PR-004 — Composed Execution Capsule.** At minimum: executable GGen CLI, GGen Marketplace
  packs, required runtime dependencies, stable marketplace root, sufficient dependencies for
  admission/evidence execution (`/usr/local/bin/ggen`, `/opt/ggen-marketplace/packs/`).
- **PR-005 — Real CLI Execution.** `ggen --version` executes successfully from inside the exact
  built image. A file named `ggen` existing is not sufficient.
- **PR-006 — Marketplace Presence.** A non-empty, expected marketplace installation is
  demonstrated (`ls /opt/ggen-marketplace/packs` or a stronger semantic query).
- **PR-007 — Container-Native Manufacture.** `ggen sync run` runs *inside* the execution capsule;
  the host runner does not need a separately installed GGen executable.
- **PR-008 — Reusable GitHub Consumer Interface.** GGen Marketplace exposes a reusable
  GitHub-native interface invoking the exact ecosystem capsule, itself generated from marketplace
  semantic inputs rather than hand-authored.
- **PR-009 — Immutable Production Consumption.** Release qualification resolves the published
  capsule to an immutable digest (`ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:<digest>`); a
  `latest` tag may exist for navigation but cannot establish replay identity.
- **PR-010 — Fresh Consumer.** At least one independent consumer repository or isolated consumer
  fixture executes the canonical consumption interface without inheriting hidden local
  dependencies from the ecosystem development checkout.
- **PR-011 — No GGen Internal Knowledge Leakage.** The consumer does not encode Cargo package
  topology, sccache configuration, Rust toolchain installation, marketplace checkout path, or
  GGen build commands.
- **PR-012 — Deterministic Manufacture.** For identical `(ConsumerSHA, EcosystemDigest,
  AdmittedInputs)`, manufacture produces an equivalent deterministic consequence or an explicit
  typed refusal/failure. Silent drift is prohibited.
- **PR-013 — Doctor.** Executable diagnostic surface covering source/submodule identity, GGen
  executability, marketplace presence, lock consistency, required runtime dependencies,
  generated-output consistency, container identity where observable, missing evidence/receipt
  conditions — typed status output.
- **PR-014 — Definition of Done.** Executable, not narrative; the authoritative release decision
  is derivable from executed checks.
- **PR-015 — Chicago Qualification.** Real container, real GGen binary, real marketplace data,
  real filesystem, real consumer inputs, real generated consequences. A mock cannot establish the
  crown.
- **PR-016 — Local GitHub Actions Replay.** Generated workflows are exercisable locally with `act`
  where supported, supplementary to (not a replacement for) real GitHub execution.
- **PR-017 — Minimal GitHub Permissions.** `contents: read` / `packages: write` for publication;
  construct-only workflows remain read-only unless additional authority is explicitly required.
- **PR-018 — Generated Workflow Ownership.** Generated YAML from `ontology`/model via
  `ggen sync run` never becomes the primary editing surface.
- **PR-019 — Receipt.** Binds consumer SHA, ecosystem identity, GGen source SHA, marketplace SHA,
  container digest, admitted inputs, generated consequence digest, GGen intrinsic receipt when
  available, verifier results, execution identity, standing.
- **PR-020 — Replay.** The release receipt contains or references sufficient information for an
  authorized second environment to replay the exact manufacturing subject.
- **PR-021 — Typed Standing.** All release qualification uses `UNKNOWN` / `PARTIAL_ALIVE` /
  `ALIVE` / `BLOCKED` / `BUILD_BROKEN` / `UNSUPPORTED` / `REFUSED[typed-reason]` — no generic
  "works"/"done" state may replace release standing.

## 9. User Experience Requirements

- **UX-001 — One Discoverable Entry Surface.** `make doctor`, `make build`, `make verify`,
  `make chicago`, `make dod` (or final repository equivalents) discoverable without reading
  implementation internals.
- **UX-002 — Failures Must Point to the Broken Transition.** e.g. `CONSTRUCT -> BUILD_BROKEN[...]`,
  `RESOLVE -> BLOCKED[IMAGE_NOT_FOUND]`, `ADMIT -> REFUSED[MARKETPLACE_IDENTITY_MISMATCH]`.
- **UX-003 — No False Green.** A command must not print success when only an earlier stage
  succeeded (e.g. "container builds" must not be rendered as "release ALIVE").

## 10. Nonfunctional Requirements

- **NFR-001 Reproducibility** — exact source and execution identities recorded.
- **NFR-002 Portability** — canonical environment runs on GitHub-hosted Linux runners; local
  Docker execution provides an equivalent development boundary where architecture permits.
- **NFR-003 Security** — no consumer secret embedded into the execution image; registry
  credentials remain runner/execution concerns.
- **NFR-004 Supply-Chain Integrity** — source commit identity, image tag, image digest, and
  generated output digest are distinguished and never substituted for one another.
- **NFR-005 Failure Transparency** — qualification tooling preserves command exit codes and
  failure evidence.
- **NFR-006 Minimal Consumer State** — consumer setup approaches O(1) with respect to the number
  of GGen capabilities consumed; adding a marketplace capability does not require a new bootstrap
  mechanism.
- **NFR-007 Idempotence** — repeated deterministic manufacture from identical admitted state does
  not introduce irrelevant repository churn.
- **NFR-008 Traceability** — every release-critical requirement maps to at least one executable
  acceptance test or receipt field.

## 11. Product Metrics

- **Fresh Consumer Time to ALIVE** — `T_alive = t(ALIVE) - t(clean checkout)`; establish baseline
  in v26.8.28, do not optimize prematurely.
- **Consumer Bootstrap Complexity** — number of ecosystem-specific operations the consumer must
  encode; target direction `B_c -> 1`.
- **Consumer Knowledge Leakage** — count of ecosystem implementation facts encoded downstream;
  target `K_c = 0` for derivable toolchain facts.
- **Manual Generated Artifact Modification** — target `0`.
- **Unreceipted Actuation** — target `0`.

---

# Part II — Architecture Requirements Document

## 12. Architectural Intent

The v26.8.28 architecture establishes `ggen-ecosystem` as a **governed composition and execution
identity**, not another source monorepo:

```text
              ggen                ggen-marketplace
                |  exact gitlink        |  exact gitlink
                v                       v
                     ggen-ecosystem
                          |
                          v
                    Docker Build
                          |
                          v
               Immutable OCI Image
                          |
                          v
                GitHub Consumer Rail
                          |
                          v
                    Consumer Repo
                          |
                          v
                    ggen sync run
                          |
                          v
          Verify -> Receipt -> Standing
```

## 13. System Boundaries

- **`ggen`** owns GGen implementation identity: executable source, core behavior, source-native
  build requirements. Does not own the combined ecosystem identity.
- **`ggen-marketplace`** owns reusable executable knowledge: packs, templates, semantic
  structures, the GitHub Actions pack, reusable consumer structures. Does not absorb GGen
  implementation identity.
- **`ggen-ecosystem`** owns composition: pins, admission, qualification, transport, release
  standing. Minimal independent procedural implementation; primary authored surfaces are
  semantic/configuration/composition plus unavoidable execution packaging.
- **Consumer Repository** owns domain intent, project-specific semantic facts, irreducible local
  implementation, exact ecosystem selection where required. Does not own GGen bootstrap.
- **GHCR** is transport/storage for the execution capsule, not semantic authority. A successfully
  pushed image does not imply qualification.
- **GitHub Actions** is an execution transport, not the canonical ontology, and is not
  automatically authoritative evidence merely because a check is green.

## 14. Source Composition Architecture

```text
vendor/
  ggen/
  ggen-marketplace/
```

Each gitlink binds an exact producer commit. The architecture deliberately avoids copying source,
manually vendoring an archive, inferring current HEAD, or floating `main`. This transitioned the
composition root from URL/SHA-only references in TOML to real git submodules for both producers.

## 15. Marketplace Resolution Architecture

Where supported by GGen configuration, packs resolve against the vendored marketplace path:

```toml
[packs]
github-actions = { path = "vendor/ggen-marketplace/packs/github-actions-pack" }
```

Local `path` pack sources are a real, confirmed-supported GGen manifest schema form (verified
against `ggen`'s own `crates/ggen-config/src/config_schema.rs` test fixtures), not an assumption.
This gives construction a source identity already bound by the composition root.

## 16. Container Architecture

### 16.1 Builder Stage

```text
load exact vendor/ggen tree
  -> install exact required Rust/toolchain environment
  -> honor repository build configuration (sccache, pinned nightly)
  -> compile actual CLI by unambiguous manifest path
  -> place executable into controlled output path
```

Where Cargo package naming is ambiguous, the build selects by exact manifest path rather than
relying on downstream knowledge of package-name resolution:

```bash
cargo build --release --locked \
  --manifest-path crates/ggen-cli/Cargo.toml --bin ggen
```

This form was chosen only after two real, confirmed build failures: `crates/ggen-cli`'s package
`name` is `ggen` (not `ggen-cli`, the directory name), and the *workspace root* `Cargo.toml` also
declares `name = "ggen"` — a duplicate package name that makes `-p ggen` resolve ambiguously to
the wrong package. `--manifest-path` disambiguates by path instead of name.

See `docs/GGEN-BUILD-CONTRACT.md` for the full canonical build contract (exact invocation,
required system packages, and all three verified build-topology gotchas).

### 16.2 Final Stage

```text
GGen executable
marketplace packs
git
python3
CA certificates
only other proven runtime prerequisites
```

`git` and `python3` are real, confirmed runtime dependencies of the admission/evidence workflow
steps that now execute inside this container (submodule-drift `git rev-parse` checks, inline
Python pack-admission/receipt-binding scripts) — not speculative additions.

### 16.3 Marketplace Root

```text
GGEN_MARKETPLACE_ROOT=/opt/ggen-marketplace
```

Consumers do not pass host-specific marketplace locations.

## 17. Container Identity

```text
repository SHA != image tag != image digest != executable digest
```

All may appear in provenance. Release consumption is ultimately bound to the OCI digest.

## 18. GitHub Workflow Architecture

- **18.1 Ecosystem Container Workflow** (`ggen-ecosystem-container.yml`): checkout exact source +
  submodules, build image, authenticate GHCR, push image, resolve digest, emit provenance.
- **18.2 Ecosystem Manufacture Workflow** (`ggen-ecosystem-sync.yml`): checkout exact candidate,
  admit exact ecosystem/marketplace identity, execute the `construct` job **inside** the composed
  GGen ecosystem container, run `ggen sync run`, bind generated consequence, emit evidence, keep
  repository mutation authority external/read-only (`contents: read`).

## 19. Reusable Action Architecture

The reusable consumer Action belongs to marketplace executable knowledge:

```bash
docker run --rm \
  -v "${GITHUB_WORKSPACE}:/workspace" -w /workspace \
  ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:<digest> \
  ggen sync run
```

Exact arguments are generated from the action vocabulary/interface (`gha:CompositeAction`
individuals rendered by `composite_action.yml.tmpl`), not hand-authored — mount the GitHub
workspace, execute inside the composed image, avoid a consumer binary install.

## 20. Authority Architecture

```text
SELECT != CONSTRUCT != DO
```

- **SELECT** — resolve/admit the desired ecosystem and manufacturing subject; no mutation
  authority implied.
- **CONSTRUCT** — generate artifacts and candidate consequences; no external write authority
  implied.
- **DO** — perform external mutations (push GHCR image, change repository state, publish release
  objects); requires explicit authority and a receipt.

## 21. BRCE Requirement

```text
Intent -> Admission -> Authority -> Execute -> Verify -> Receipt
```

Invariant: `DO => Receipt`. No successful actuation without an evidence path.

## 22. Admission Architecture

Validate before manufacture: consumer identity, ecosystem identity, GGen source identity,
marketplace source identity, required pack paths, container identity, working directory. Invalid
or inconsistent identity is a refusal, not a best-effort fallback (e.g.
`REFUSED[MARKETPLACE_SUBMODULE_DRIFT]`).

## 23. Failure Semantics

`UNKNOWN`, `PARTIAL_ALIVE`, `BUILD_BROKEN`, `BLOCKED`, `UNSUPPORTED`, `REFUSED[...]`, `ALIVE` — as
defined in `docs/STANDING.md`. A build failure is evidence and feeds repair, not a project
failure.

## 24. Doctor Architecture

```text
parse -> resolve -> admit -> construct prerequisites -> runtime prerequisites
      -> verification prerequisites -> receipt prerequisites
```

Reports the earliest failed transition and preserves independent later observations where useful
(see `scripts/doctor.sh`).

## 25. Definition-of-Done Architecture

```text
DoD_26.8.28 = AND over all Gate_i
```

Required gates: source identity, submodules, container build, CLI execution, marketplace
visibility, `ggen sync run`, generated-output verification, doctor, Chicago test, local workflow
execution where applicable, GHCR push, digest resolution, fresh consumer, receipt, replay. A
missing mandatory gate means the release is not `ALIVE`. See `docs/DEFINITION-OF-DONE.md`.

## 26. Chicago Test Architecture

```text
build exact image -> mount fixture -> execute real ggen -> run sync
  -> inspect output -> verify expected consequence -> verify receipt
```

Preferred fixture layout: `tests/fixtures/consumer/{ggen.toml, semantic input...}`. See
`tests/test_container_smoke.sh` — its existence alone does not establish successful execution;
only a real, currently-passing run does.

## 27. DX Architecture

DX commands compose existing canonical operations (`make doctor`, `make build`, `make chicago`,
`make dod`, ...) — the `Makefile` may orchestrate; it must not become an independent
implementation of release logic.

## 28. Receipt Schema

```json
{
  "subject": { "repository": "...", "commit": "..." },
  "ecosystem": {
    "version": "v26.8.28",
    "ggen_commit": "...",
    "marketplace_commit": "...",
    "container_digest": "sha256:..."
  },
  "admission": { "result": "ADMITTED" },
  "execution": { "command": "ggen sync run", "exit_code": 0 },
  "consequence": { "digest": "..." },
  "verification": { "doctor": "ALIVE", "chicago": "ALIVE", "dod": "ALIVE" },
  "standing": "ALIVE"
}
```

Exact schema may be RDF/JSON or another existing GGen receipt form; the semantic obligations
matter more than this illustrative serialization.

## 29. Replay Architecture

```text
R = ConsumerSHA + EcosystemDigest + AdmittedInputs + CommandContract
```

Replay output either reproduces the qualified consequence or exposes a typed reason it cannot.
Replay may never silently substitute a newer ecosystem version.

## 30. Security Architecture

Publishing requires package write authority; consumption requires only image-visibility access.
Construct workflow remains `contents: read` where no repository actuation is required. Never
embed GitHub tokens, registry passwords, private SSH keys, or consumer secrets in the container.
Marketplace contents are executable manufacturing knowledge and must be identity-bound; a
marketplace mismatch is an integrity failure.

## 31. Supply-Chain Architecture

```text
ggen commit -\
              -> ecosystem source -> image digest -\
marketplace commit -/                                -> consumer execution -\
consumer commit -----------------------------------------------------------> receipt
verification identity ------------------------------------------------------/
```

Each edge must be inspectable.

## 32. Generated Artifact Rule

For a generated workflow: semantic source is authority, generated YAML is consequence. For a
generated reusable Action: marketplace semantic source is authority, `action.yml` is consequence.
Hand-editing the consequence introduces divergence and should be refused by release policy or
detected by verification.

## 33. Release Qualification Ladder

```text
L0  static identity                 L8  doctor
L1  submodule closure               L9  Chicago/full-loop container test
L2  semantic/admission validation   L10 local act execution
L3  container build                 L11 GHCR publish
L4  ggen --version                  L12 digest-bound pull
L5  marketplace visibility          L13 independent consumer
L6  local ggen sync run             L14 receipt validation
L7  generated consequence verification  L15 replay
```

Do not rerun an unchanged failed transition without a new hypothesis or repair.

## 34. Required Falsifiers

Wrong GGen commit, wrong marketplace commit, dirty/mismatched gitlink, missing marketplace,
missing python runtime, missing GGen executable, wrong image digest, invalid working directory,
failed `ggen sync`, generated artifact drift, missing receipt — each must produce a typed failure
or refusal.

## 35. Fresh Consumer Crown Test

**Preconditions**: a consumer exists independently of the composition-root development
environment, with only legitimate consumer state, no preinstalled GGen executable, no preinstalled
marketplace checkout.

**Actuation**: the consumer invokes the canonical reusable GitHub-native interface using the exact
ecosystem identity.

**Required observations**: exact consumer SHA observed; exact ecosystem digest resolved; exact
marketplace identity admitted; real GGen process starts; real marketplace pack resolves;
`ggen sync run` exits successfully; expected output is produced; output satisfies verifier;
receipt is produced; replay information exists.

**Terminal state**: `OBSERVED / ADMITTED / CONSTRUCTED / EXECUTED / VERIFIED / RECEIPTED /
REPLAYABLE` all true, `CHANGED` as expected, `STANDING = ALIVE`.

## 36. Release Acceptance Matrix

See `docs/DEFINITION-OF-DONE.md` for the live, executed version of this matrix (same `PR-###`
ids, with real evidence or an honest `UNKNOWN`/`BLOCKED` per row instead of an aspirational
"Required Standing" column).

## 37. Release Blockers

Container cannot be built; GGen cannot execute inside the exact image; marketplace cannot be
resolved from the image; consumer still downloads GGen; consumer requires local GGen source
knowledge; registry artifact has no immutable digest; exact source identities cannot be
reproduced; canonical consumer does not execute; DoD does not execute; Chicago boundary is mocked
rather than real; no receipt exists; release state depends on assertion rather than evidence.

## 38. Scope-Fence Policy

```text
Failure -> Locate Transition -> Repair Narrowest Cause -> Encode Permanent Guard -> Rerun
```

Do not convert a narrow build issue into unrelated architecture work. Conversely, if a failure
exposes reusable manufacturing knowledge (e.g. the Cargo CLI package-selection discovery in
Section 16.1), promote it to its canonical layer rather than letting every future consumer
rediscover it independently.

## 39. Release Deliverables

```text
ggen-ecosystem/
|-- .gitmodules
|-- vendor/{ggen, ggen-marketplace}
|-- ggen.toml
|-- ecosystem.lock.toml
|-- ontology.ttl
|-- Dockerfile
|-- .dockerignore
|-- .actrc
|-- Makefile
|-- scripts/doctor.sh
|-- tests/{test_container_smoke.sh, fixtures/...}
|-- docs/{PRD-ARD-v26.8.28.md, DEFINITION-OF-DONE.md}
|-- receipts/...
`-- .github/workflows/{ggen-ecosystem-container.yml, ggen-ecosystem-sync.yml}
```

Generated files remain generated consequences. The exact final tree may differ where repository
doctrine requires it.

## 40. Definition of Release Completion

```text
FreshConsumer x ExactEcosystem --GitHub--> Manufacture --Verification--> Receipt --Replay--> ALIVE
```

and no hidden GGen bootstrap knowledge is required outside the ecosystem boundary. In plain
language: a clean repository can use one exact GGen ecosystem identity to manufacture itself
through GitHub Actions, using the real GGen implementation and real marketplace knowledge, with no
standalone binary installation, and produce evidence sufficient to prove and replay the exact
result.

## 41. v26.8.28 → Vision 2030

v26.8.28 establishes only the first foundational closure: the **Portable Manufacturing Machine**.
Once it is `ALIVE`, subsequent releases can attack consumer fanout, repository inversion,
capability closure, executable industry knowledge, knowledge hooks, defect-class elimination, and
autonomic software manufacturing. The strategic importance of v26.8.28 is not the container
itself — it establishes the invariant that the manufacturing environment can be named,
transported, independently executed, falsified, receipted, and replayed as a single ecosystem
artifact.
