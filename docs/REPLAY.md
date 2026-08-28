# Replay

Replay reconstructs the same admitted subject; adjacency is not replay.

## Required identity
- `ggen-ecosystem` source SHA
- GGen release `v26.8.27` and source commit `df1e138a64c80e41090cff7c84fb62d77e03b734`
- Linux asset SHA-256 from `ecosystem.lock.toml`
- marketplace SHA `4c4232515b43d40cef8288c43eacfab2c31ab485`
- `ggen.toml` and `ontology.ttl`
- selected semantic profile/catalog closure
- pack closure
- receipt/evidence chain

## Canonical proven replay rail

Use `.github/workflows/ggen-ecosystem-sync.yml` with the exact values recorded in `ecosystem.lock.toml`. The workflow verifies the release asset before executing `ggen sync run`, captures the generated patch and receipt inputs, and emits an evidence artifact without repository write authority.

Local or sibling-checkout replay is also lawful when it resolves to the exact same producer/pack identities. A replay that silently moves any identity is a different experiment.
