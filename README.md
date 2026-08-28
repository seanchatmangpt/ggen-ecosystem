# ggen-ecosystem

`ggen-ecosystem` is the canonical governed composition root for the GitHub-hosted ggen ecosystem.

It owns **ecosystem identity, topology, admission, closure, qualification, transport, profile selection, release standing, and replay coordinates**. It does not absorb the source identity of `ggen`, `ggen-marketplace`, or independently versioned ecosystem repositories.

## System equation

```text
observed GitHub graph + public ontology
    -> admitted ecosystem graph O*
    -> DfCM selection / construction
    -> ggen + marketplace packs
    -> deterministic artifacts
    -> BRCE-bounded actuation
    -> receipt + replay
    -> scoped standing
```

The root manufacturing command is:

```bash
ggen sync run
ggen receipt verify
ggen sync run --dry-run
```

`ggen` and `ggen-marketplace` are resolved as sibling checkouts at the exact SHAs recorded in `ecosystem.lock.toml`.

## Ownership

| Surface | Ownership |
|---|---|
| `ggen` | deterministic graph-backed manufacturing engine |
| `ggen-marketplace` | accumulated executable knowledge / reusable packs |
| ecosystem repositories | independently versioned products, libraries, gyms, services, adapters |
| `ggen-ecosystem` | canonical composition, admission, closure, qualification, transport, standing |

## DfCM law

The repository follows:

1. **Preserve** — retain lawful reversible options.
2. **Fence** — preserve semantics and Chesterton obligations before removal.
3. **Calculus** — model objects, morphisms, admission, closure, authority, actuation, receipt, replay, standing.
4. **Exclusions** — refuse ambient execution, projection authority, hook actuation, and unreceipted mutation.
5. **Falsifier** — every crown claim names a falsifier.
6. **Extension** — add repositories, packs, profiles, runtimes, proofs, and transports without bypassing the calculus.
7. **Operationalization** — graph -> query -> ggen -> runtime -> BRCE -> receipt -> replay -> standing.

`SELECT != CONSTRUCT != DO`. Source graphs, generated projections, planners, hooks, and CI metadata have no ambient DO authority.

## Source vs projection

Authoritative editing surfaces:

- `ecosystem.ttl`
- `ontology/*.ttl`
- `profiles/*.ttl`
- `admission/*.ttl`
- `ecosystem.lock.toml`
- `ggen.toml`

Generated artifacts belong under `generated/`, `consumer/`, and `.ggen-v2/`. Generated artifacts are projections and evidence, never the canonical ecosystem ontology.

## Profiles

Profiles are semantic subsets over one graph, not forks of truth:

- `cloud-session` — portable bootstrap closure for cloud coding sessions.
- `platform-engineering` — XaaS/platform/runtime/delivery/governance closure.
- `process-intelligence` — ex4pm/wasm4pm/PM/verification closure.
- `autofde` — AutoFDE/gym/certification simulation closure.
- `everything` — maximal bounded ecosystem closure.

See `docs/PROFILES.md`.

## Standing

`ALIVE` is reserved for observed execution against the exact admitted subject. Repository presence, configuration, workflow existence, or a green unrelated check is insufficient.

See `docs/STANDING.md` and `receipts/README.md`.
