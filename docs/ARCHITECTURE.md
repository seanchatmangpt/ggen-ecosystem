# Architecture

## Root contract

`ggen-ecosystem` is a **composition root**, not a source monorepo.

```text
GitHub repositories
    -> observed repository/capability graph
    -> admission + exclusions
    -> profile/closure selection
    -> exact external lock
    -> ggen pack composition
    -> generated projection
    -> BRCE actuation
    -> BLAKE3 receipt
    -> replay
    -> standing
```

### Objects
Repositories, packs, capabilities, profiles, candidates, policies, receipts, evidence, standing claims.

### Morphisms
`dependsOn`, `providesCapability`, `includesRepository`, `includesPack`, `includesCapability`, `manufacturedBy`, `verifiedBy`.

### Admission
SHACL and pack gates constrain the graph. UNKNOWN is not admitted merely because it is plausible.

### Closure
A profile resolves to a dependency-closed set of repositories, packs, and capabilities. The exact external identities are pinned separately in `ecosystem.lock.toml`.

### Authority
Ontology, planners, queries, templates, generated projections, hooks, and CI metadata may SELECT or CONSTRUCT. They do not receive ambient DO authority.

### Actuation
Irreversible mutation routes only through an admitted receipted broker.

### Receipt/replay
A receipt binds subject identity, graph, outputs, authority and consequence. Replay must test the same admitted subject boundary.

### Standing
Only observed exact-subject execution may crown `ALIVE`.

## Extension rule

New repositories and packs enter first as reversible graph facts or candidates. Their addition does not require centralizing their source. Removing an existing relation requires a semantic fence: preserve why it existed, the equivalence relation under which it can be removed, and a falsifier for the replacement.


## Public census boundary

The repository census is an observation surface, not an admission oracle. Public repositories that are plausibly ecosystem-relevant are retained as `RepositoryCandidate` nodes with `CANDIDATE` standing. They do not acquire dependency, capability, profile, or actuation authority merely by adjacency. Non-public repository identities are not projected into this public repository: observation authority is not publication authority.
