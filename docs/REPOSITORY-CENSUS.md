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

## Local-project audit extension — 2026-08-29

"Audit all of my projects for consideration" was executed as a second, narrower census pass on
top of the 2026-08-28 owner-estate closure above: the same `gh api user/repos` owner enumeration,
re-run fresh (`379` owned / `301` public / `78` private -- `+1`/`+1`/`+0` vs. the prior day),
filtered to the **real-work audit population** `visibility=public AND fork=false AND
archived=false` (`134` repositories) rather than the raw public-catalog cardinality. Forks and
archived repositories are excluded from this population because they are not "my projects" in the
authored-work sense this request asked about, even though they remain in the broader public
catalog scope.

Diffing that 134-repository population against the `dcterms:identifier` values already present in
`ontology/repositories.ttl` (3 constitutional repositories) and `ontology/repository-census-01.ttl`
through `-04.ttl` (66 previously materialized candidates) produced a gap of **87** repositories with
no census representation. Each was materialized as an `eco:RepositoryCandidate` individual, using
the identical predicate shape as the existing shards (`dcterms:identifier`, `eco:sourceUrl`,
`eco:censusStanding "CANDIDATE"`, `eco:membershipBasis`, `eco:publicProjection true`), across six
new shards: `ontology/repository-census-05.ttl` through `-10.ttl`.

This is deliberately **mechanical, not judgment-based** materialization, matching the existing
shards' own convention: candidacy here means "observed, real, owned, public, non-fork, non-archived
repository" only -- it is not a relevance or profile-fit judgment, which the Promotion pipeline
below still gates separately.

The full merged graph (10 census shards + `ontology/repositories.ttl`, 1123 quads across 11 files)
was validated for real with the ecosystem's own build-facing RDF/SHACL validator:

```text
ggen graph validate \
  --files ontology/repositories.ttl,ontology/repository-census-01.ttl,...,ontology/repository-census-10.ttl \
  --shapes admission/shapes.ttl
# -> files_checked: 11, shapes_checked: 1, shapes_conform: true on every file, 0 duplicate identifiers
```

22 previously materialized candidates from the 2026-08-28 shards fall outside the current
`fork=false AND archived=false` population (e.g. `ash`, `ash_events`, `ash_postgres`, `pm4py`,
`POWL`, `weaver`, `xaas`). Per the fix-forward discipline, these are left admitted as-is rather
than removed.

### Reverification of the 22 flagged candidates — same day, 2026-08-29

Each of the 22 was individually re-queried (`gh api repos/seanchatmangpt/<name>`, a per-repository
GET rather than the paged list enumeration) to close the "not yet independently re-verified"
caveat above. Result: **all 22 are confirmed real, public, non-archived forks** of other owners'
repositories -- `seanchatmangpt/ash` forks `ash-project/ash`, `seanchatmangpt/oxigraph` forks
`oxigraph/oxigraph`, `seanchatmangpt/weaver` forks `open-telemetry/weaver`, `seanchatmangpt/tcps`
forks `github/spec-kit`, and so on for the full 22 (see the `fork_map` in
`receipts/github-ecosystem-census-2026-08-29.json`). None were renamed, deleted, transferred, or
turned private -- every lookup succeeded and the fork explanation accounts for all 22.

Each of the 22 `eco:RepositoryCandidate` individuals was updated in place: `eco:censusStanding`
stays `"CANDIDATE"` (required by `admission/shapes.ttl`'s `RepositoryCandidateShape`, and the
repository genuinely is still an observed public repository), but each now also carries a new
`eco:forkOf "<upstream full_name>"` fact, a new `eco:censusReverifiedDate "2026-08-29"^^xsd:date`,
and an `eco:membershipBasis` updated to record the verified fork status and its exclusion from the
authored-work audit population. The `eco:forkOf` and `eco:censusReverifiedDate` predicates are
declared in `ontology/repository-census.ttl` alongside the pre-existing census vocabulary.

Post-update, the full merged graph (still 11 files) was re-validated with
`ggen graph validate --shapes admission/shapes.ttl`: `files_checked=11`, `shapes_conform=true` on
every file, `RepositoryCandidate` count unchanged at 153, zero duplicate `dcterms:identifier`
values -- the reverification added facts without disturbing any existing admission state.

The exact machine receipt for both passes is `receipts/github-ecosystem-census-2026-08-29.json`.

### Post-audit delta — shard 11, 2026-08-29 (local) / 2026-08-30T01:04Z (GitHub)

`ontology/repository-census-11.ttl` records one repository created after the shard-05..10
enumeration ran and therefore absent from it: `seanchatmangpt/beam4pm` (verified individually via
`gh api repos/seanchatmangpt/beam4pm`: public, non-fork, non-archived, created
2026-08-30T01:04Z). It is the first ggen-only manufactured product proof — its application source
is projected by `ggen sync run` from its own `ontology.ttl` through the
`beam4pm-process-model-pack` vendored from `ggen-marketplace`. Census standing is `CANDIDATE`
like every other observation; manufacturing standing lives in that repository's own receipts, not
here. Shard 11 validated against `admission/shapes.ttl` (`shapes_conform=true`, 8 quads).

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
