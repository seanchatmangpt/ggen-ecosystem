# Replay

Replay reconstructs the same admitted subject; adjacency is not replay.

## Required identity
- `ggen-ecosystem` commit SHA
- exact `ggen` SHA
- exact `ggen-marketplace` SHA
- `ggen.toml`
- ontology imports
- selected profile
- pack closure
- toolchain identity
- receipt chain

## Canonical sibling layout

```text
workspace/
  ggen/
  ggen-marketplace/
  ggen-ecosystem/
```

At the ecosystem root:

```bash
ggen sync run
ggen receipt verify
ggen sync run --dry-run
```

A replay that silently moves either external SHA is a different experiment.
