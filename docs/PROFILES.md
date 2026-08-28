# Profiles

Profiles are semantic projections over one canonical graph. They are not divergent configuration forks.

| Profile | Intent | Initial standing |
|---|---|---|
| `cloud-session` | portable deterministic cloud bootstrap | CANDIDATE |
| `platform-engineering` | platform/XaaS closure | CANDIDATE |
| `process-intelligence` | process intelligence / conformance closure | CANDIDATE |
| `autofde` | AutoFDE and gym closure | CANDIDATE |
| `everything` | maximum bounded ecosystem closure | CANDIDATE |

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
