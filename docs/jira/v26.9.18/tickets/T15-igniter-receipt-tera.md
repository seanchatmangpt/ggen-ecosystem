# T15 — ggen_igniter: portable receipt envelope + recursive .tera discovery

- Repo: `seanchatmangpt/ggen_igniter` (worktree: `~/wt-v26918/ign-15-receipt-tera`)
- Branch: `gpack/ign-15-receipt-tera` (pre-created off `origin/main` = `15305cea`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§55, §20, §86 steps 7+8+10+14)

## Goal

Two §86 steps in one ticket (same module neighborhood): (a) emit the §55
portable receipt envelope; (b) recursive template discovery with `.tera`
routed through the repo's REAL Tera/WASM engine and explicit renderer
identity — `.tmpl` ambiguity removed under portable profiles.

## Scope

1. Receipt envelope: same field law as Rust T10 — all §54 fields, §82
   standing vocabulary, engine.name = the Igniter engine's own identity,
   `spec: "RFC-GPACK-001-v26.9.17"`. Reconciliation receipts (§59) stay as
   the Igniter extension, referenced not merged (§56).
2. Template discovery: recursive walk under `templates/` (today likely
   flat); `.tera` → Tera/WASM engine; `.eex` → EEx; `.tmpl` under portable
   profile ⇒ `REFUSED:RENDERER_AMBIGUOUS` unless frontmatter `renderer:`
   disambiguates (§22); under legacy profile `.tmpl` keeps today's
   behavior exactly.
3. Tests:
   - nested `templates/sub/dir/x.txt.tera` renders to its target (the
     recursion witness).
   - `.tera` pack renders via Tera with a Tera-only construct (e.g.
     `{% if %}`) — proving engine routing, not EEx.
   - portable-profile `.tmpl` without renderer ⇒ typed refusal; with
     `renderer: tera1` ⇒ renders.
   - legacy-profile `.tmpl` behavior unchanged (compat witness).
   - envelope: happy path has all §54 keys; refused sync carries typed
     REFUSED + standing REFUSED (§57 falsifier).
4. Inversion witness on the renderer refusal.

## Acceptance

Real `mix test` (changed scope) exit 0 + all five witnesses in History.

## Out of scope

Gate semantics (T12), manifest (T13), bindings (T14); changing the WASM
Tera engine itself.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
