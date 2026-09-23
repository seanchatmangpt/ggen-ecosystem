# T05 — marketplace catalog projection increment (#87, additive)

- Repo: `seanchatmangpt/ggen-marketplace` (worktree: `~/wt-v26918/mkt-05-catalog`)
- Branch: `gpack/mkt-05-catalog` (pre-created off `origin/main` = `800b8c6c5`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md`

## Goal

First #87 increment: where the marketplace keeps a hard-coded side table for
pack metadata (pack class / lifecycle / capabilities), make the catalog
ABLE to project those fields from pack-owned RDF (gp: vocabulary, T01) when
present, falling back to the side table when absent. Additive only; zero
legacy pack changes; §67 "stricter admission MUST NOT redefine Core identity".

## Scope

1. FIND the side table first (grep the repo for hard-coded pack class /
   capability / lifecycle maps — likely under `packages/` or a catalog
   builder). Record its path in the ticket History before changing anything.
2. Add a read path: if a pack's ontology.ttl declares
   `<urn:ggen:pack:<name>> gp:lifecycle ?l` / `gp:PackClass` /
   `gp:providesCapability`, the catalog projection emits those values for
   that pack; otherwise today's behavior, byte-identical.
3. Wire it for exactly ONE pack: `ggen-pack-spec-pack` (T01's, may be assumed
   present at merge time — code defensively if absent).
4. Tests: (a) RDF-projected pack yields RDF values; (b) a legacy pack yields
   byte-identical old output (the compatibility falsifier); (c) conflict
   (RDF says one thing, side table another) → RDF wins for projected packs
   and the diff is visible in test output.

## Acceptance (falsifiers)

1. The repo's own catalog/validation test suite runs green (real command +
   exit code in History). If no suite covers the catalog builder, add the
   3 tests above in the repo's existing test style and run them.
2. Diff of regenerated catalog output shows changes ONLY for
   ggen-pack-spec-pack (or no diff if that pack is absent — both outcomes
   recorded honestly).

## Out of scope

Migrating legacy packs off side tables; deleting the side tables; any
admission-rule change.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:02:40Z (orient) | UNKNOWN | gpack/mkt-05-catalog@800b8c6c5 | SIDE_TABLE_FOUND (pre-change, per Scope 1): `scripts/marketplace.py` — `DEPRECATED_PACKS` (l43-52, lifecycle: deprecated flag + successors) and `PACK_CLASSES` (l59-70, pack class), consumed in `Pack.catalog_record()` at l118/l130/l134. No `gp:` vocabulary anywhere in packs/ yet; `ggen-pack-spec-pack` ABSENT in this worktree (T01 owns it; code defensively). Baseline captured: `python3.11 scripts/marketplace.py catalog --scope all > /tmp/t05_catalog_before.json` exit=0 (604874 bytes) | implement gp: read path + 3 falsifiers + validation loop |
