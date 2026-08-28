# Complete GitHub ecosystem catalog

The maximal ecosystem boundary is the complete **public** GitHub owner catalog:

```text
owner = seanchatmangpt AND visibility = public
```

This predicate is canonical. A static list is only a time-stamped projection and cannot define the ecosystem because repositories may be created after the list is generated.

## Admission semantics

Catalog membership means **OBSERVED_SCOPE** only. It does not imply:

- dependency admission;
- profile compatibility;
- pack compatibility;
- buildability;
- execution;
- write authority;
- `ALIVE` standing.

The materialized repository candidates under `ontology/repository-census-*.ttl` are the initial high-signal priority subset. `eco:everything` additionally selects `eco:github-owner-catalog`, so the maximal profile denotes the whole public owner graph while preserving reversible relation-scoped promotion.

Private repository identities are intentionally absent from this public repository. Read authority is not publication authority.
