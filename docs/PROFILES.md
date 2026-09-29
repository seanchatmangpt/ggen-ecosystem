# Profiles

Profiles are semantic projections over one canonical graph. They are not divergent configuration forks.

| Profile | Intent | Initial standing |
|---|---|---|
| `cloud-session` | portable deterministic cloud bootstrap | CANDIDATE |
| `platform-engineering` | platform/XaaS closure | CANDIDATE |
| `process-intelligence` | process intelligence / conformance closure | CANDIDATE |
| `autofde` | AutoFDE and gym closure | CANDIDATE |
| `everything` | maximum bounded ecosystem closure | CANDIDATE |
| `castle` | project CASTLE's non-owner capability estate into existing irreducible owners | CANDIDATE |

## Why profiles are data

A profile selects capabilities/repositories/packs. The selection is queryable and can be projected into transport or runtime-specific manifests without making those manifests authoritative.

`everything` intentionally contains candidate packs that are not loaded by the root `ggen.toml`. This preserves the maximal option graph without pretending pack-to-pack compatibility has already been executed and verified.

Promotion rule:

```text
CANDIDATE profile edge
  -> pack gates close
  -> exact consumer sync executes
  -> receipt verifies
  -> replay is byte-identical
  -> edge may be promoted
```


## CASTLE projection profile

`castle` is intentionally different from the runtime-oriented profiles. It selects the 23 repositories that CASTLE's v26.9.28 sJira crown did not retain as irreducible `KEEP` owners and projects their useful capabilities toward existing owners.

The semantic source is `ontology/castle-projection.ttl`; `profiles/castle.ttl` selects it. Every edge remains `CANDIDATE`, stops at `CONSTRUCT`, and carries an explicit disposition, target, runtime placement, and falsifier.

The profile must not create a new runtime crown or consequence crown. XaaS remains runtime existence/composition and CASTLE remains consequential admissibility.
