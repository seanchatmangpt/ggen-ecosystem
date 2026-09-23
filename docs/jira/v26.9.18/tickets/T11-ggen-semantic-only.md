# T11 — ggen: semantic-only Core packs admitted (§73)

- Repo: `seanchatmangpt/ggen` (worktree: `~/wt-v26918/ggen-11-semantic-only`)
- Branch: `gpack/ggen-11-semantic-only` (pre-created off `origin/main` = `ad3a7e661`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§73, §12.1, §96)

## Goal

RFC §85 step 5: support semantic-only Core packs — `pack.toml` + `ontology.ttl`
with NO templates/ is a lawful pack. `Pack ⇏ Template` (§73). If ggen
currently errors on missing templates ("no templates found" or equivalent),
that error must become admission success with zero consequences.

## Scope

1. Find the "no templates" failure path. For a pack that has ontology.ttl +
   valid pack.toml and zero template files: sync succeeds, gate set still
   runs (gates are lawful in semantic-only packs), zero consequences,
   receipt standing reports the no-op honestly (not "success" implying
   writes).
2. A pack with NEITHER ontology.ttl NOR templates still fails
   (REFUSED:PACK_GRAPH_MISSING — Core requires ontology.ttl, §12.1). The
   distinction is the falsifier.
3. Tests:
   - `semantic_only_pack_admitted`: minimal Core pack, no templates →
     sync exit 0, no writes, gates executed (add one passing gate to prove
     gates still run).
   - `empty_pack_refused`: no ontology.ttl → typed refusal.
   - Legacy packs with templates: suite green unchanged (compat witness).
4. §96 "Renderer identity" row is out of your path; do not touch template
   discovery beyond the empty-set case.

## Acceptance

Real `cargo test` (changed scope) exit 0 + the three witnesses in History,
including the inverted-run note for the admitted/refused pair.

## Out of scope

Igniter (its §73 UNSUPPORTED reporting is T12–T15 territory); marketplace;
dependency graphs.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
