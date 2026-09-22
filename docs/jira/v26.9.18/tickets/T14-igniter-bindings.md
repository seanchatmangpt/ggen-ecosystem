# T14 — ggen_igniter: canonical RDF binding normalization (D6, §23/§24)

- Repo: `seanchatmangpt/ggen_igniter` (worktree: `~/wt-v26918/ign-14-bindings`)
- Branch: `gpack/ign-14-bindings` (pre-created off `origin/main` = `15305cea`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§23, §24, §86 step 11, D6)

## Goal

Resolve D6: Igniter supports multiple SPARQL engines whose lexical forms
differ (quoted IRIs vs bare, typed literals vs plain). Normalize every
engine's result rows into the §23/§24 canonical typed binding model BEFORE
templates see them: `{type: uri|bnode|literal, value, datatype?, xml:lang?}`
per term, `unbound` = absent key.

## Scope

1. A normalization layer between query execution and render bindings, with
   one adapter per supported engine (find them via the repo's engine
   selection code). All engines funnel through the same canonical struct.
2. Render templates from the canonical form (convenience scalar views MAY
   be provided, §24 — canonical form is the comparison oracle).
3. Tests per §23 term kind (these mirror the spec-pack vectors, T04):
   - IRI → `{"type":"uri","value":"https://…"}` — assert NO angle brackets
     and NO quotes leak into value from ANY engine.
   - simple literal → type literal, no datatype key.
   - `"42"^^xsd:integer` → value "42" (string), datatype IRI present.
   - `"chat"@en` → xml:lang "en".
   - unbound/OPTIONAL-miss → key absent.
   - CROSS-ENGINE witness: run the same vector through ≥2 engines the repo
     supports and assert IDENTICAL canonical maps (this is the D6
     falsifier; if only one engine is testable in this environment, record
     PARTIAL_ALIVE with the exact blocker).
4. Template authors' existing packs keep rendering (compat witness: one
   existing pack test green).

## Acceptance

Real `mix test` (changed scope) exit 0 + per-kind witnesses + the
cross-engine result honestly recorded in History.

## Out of scope

Rust-side bindings (T10 envelope only references them); result ordering
(§25 — already covered by ORDER BY discipline in fixtures); receipts (T15).

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
