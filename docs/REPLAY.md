# Replay

Replay reconstructs the same admitted subject; adjacency is not replay.

## Required identity
- `ggen-ecosystem` source SHA (`subject.commit` — full 40-char git SHA, per `docs/RECEIPT-SCHEMA.md`)
- GGen release `v26.8.28` and source commit `c61ee99359c9dbc7b3cb71687976932a3e737ed4` (`ecosystem.ggen_commit` in `ecosystem.lock.toml` / a receipt)
- container image digest (`ecosystem.container_digest`, `sha256:<64-hex>` form) — this is the identity `tests/replay_check.sh` actually pins and resolves locally; it never pulls or falls back to a tag/HEAD. As of `ecosystem.lock.toml`, the composed image at digest `sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c` is `BLOCKED[manifest-unknown]` (observed on hosted run 33238309149) — not currently a pullable capsule. Republish before treating that digest as replayable.
- marketplace SHA `89adf4c8476f7edc8067fdbb1c256cfbfa22df6a` (`ecosystem.marketplace_commit`)
- `ggen.toml` and `ontology.ttl`
- selected semantic profile/catalog closure
- pack closure
- receipt/evidence chain (a receipt matching the field contract in `docs/RECEIPT-SCHEMA.md`)

## Canonical proven replay rail

Use `.github/workflows/ggen-ecosystem-sync.yml` with the exact values recorded in `ecosystem.lock.toml`. The workflow verifies the release asset before executing `ggen sync run`, captures the generated patch and receipt inputs, and emits an evidence artifact without repository write authority.

Local or sibling-checkout replay is also lawful when it resolves to the exact same producer/pack identities. A replay that silently moves any identity is a different experiment.

## Verifying a replay against a receipt

`tests/replay_check.sh <receipt.json>` is the executable replay contract (PR-020). Given a
receipt matching `docs/RECEIPT-SCHEMA.md`, it extracts `ecosystem.container_digest`,
`subject.commit`, `execution.command`, and `consequence.digest`; resolves the image digest
locally only (no `docker pull`); materializes `subject.commit`'s exact tree via a scratch
git worktree with submodules initialized; re-runs `execution.command` against that exact
image digest; and compares the sha256 of the replayed command's stdout against the recorded
`consequence.digest` (stderr is captured separately for diagnostics but excluded from the
hash, since it carries non-deterministic timestamps/durations). It refuses — a typed
`REFUSED[<reason>]` on stderr, exit code 3 — rather than substituting a newer tag, `:latest`,
or `HEAD` when the exact digest or commit is not locally available. Use `--dry-run` to see
every extracted field and every command that would run without needing a container or a
real receipt.
