# Repository census

The GitHub census is an **observation surface**, not an ecosystem-membership oracle.

The completed owner census is filtered through a publication fence before projection into this public repository:

1. non-public identities are not published merely because the observer can read them;
2. the three constitutional repositories (`ggen`, `ggen-marketplace`, `ggen-ecosystem`) are admitted in `ontology/repositories.ttl`;
3. plausibly ecosystem-relevant public repositories are preserved in `ontology/repository-census.ttl` and its shards as `RepositoryCandidate` nodes;
4. a candidate acquires no dependency, capability, profile, or actuation authority by adjacency;
5. promotion requires evidence and an explicit admission change.

This is the DfCM interpretation of a repository census: maximize lawful option capital without collapsing observation into admission.

## Exact owner-estate closure — 2026-08-28

The connected GitHub account was enumerated to exhaustion rather than sampled.

```text
owned repositories observed = 378
public repositories          = 300
private repositories         = 78
                               ---
                               378
```

The exact-set cardinality was falsified at the collection boundary:

- owner enumeration used pages of 100 repositories: zero-based pages `0`, `1`, `2`, and `3` were non-empty; page `4` was empty;
- zero-based owner item `377` exists; item `378` does not;
- one-based public item `300` exists; item `301` does not;
- one-based private item `78` exists; item `79` does not.

The canonical public catalog therefore has a currently observed cardinality of **300**, while its durable boundary remains the predicate `owner=seanchatmangpt AND visibility=public`. A future public repository is immediately in catalog scope even before the next materialized census refresh.

The complete owned estate of 378 is **not** asserted as 378 admitted ecosystem dependencies. It is the complete observation domain from which relation-scoped candidates and admissions can be derived.

## Privacy fence

`ggen-ecosystem` is public. The 78 private observations are represented only as the protected private partition cardinality. Public ecosystem artifacts must not materialize private repository names, repository IDs, URLs, refs, SHAs, descriptions, or sizes merely because connected tooling can observe them.

The exact machine receipt is `receipts/github-ecosystem-census-2026-08-28.json`.

## Identity law

When a repository observation requires a durable identity, use the GitHub repository ID. Repository name, visibility, archived state, default branch, and branch-head SHA are mutable observations and must not be treated as durable identity.

Supply-chain inputs remain stricter: GGen, marketplace, packs, release assets, generated consequences, and replay evidence are pinned to the exact identities required by their own admission contracts.

## Promotion

```text
PUBLIC + OBSERVED
  -> CANDIDATE
  -> evidence of ecosystem role
  -> closure/admission checks
  -> exact identity pinned when required
  -> executable qualification
  -> ADMITTED for the scoped relation
```

Membership is relation-scoped. A repository can be admitted to a profile without becoming a locked manufacturing dependency of every other profile.
