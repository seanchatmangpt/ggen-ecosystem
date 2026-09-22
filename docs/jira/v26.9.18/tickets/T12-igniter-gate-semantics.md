# T12 — ggen_igniter: gates = refusal falsifiers, queries = render inputs (D1)

- Repo: `seanchatmangpt/ggen_igniter` (worktree: `~/wt-v26918/ign-12-gate-semantics`)
- Branch: `gpack/ign-12-gate-semantics` (pre-created off `origin/main` = `15305cea`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§14, §86 steps 3+5+6, D1)

## Goal

Resolve divergence D1 on the Igniter side: today `gates/*.rq` are consumed as
named rendering queries. In Igniter they MUST become refusal falsifiers with
the exact Rust semantics (SELECT ≥1 row ⇒ violation; ASK true ⇒ violation;
refusal happens BEFORE projection), plus `queries/*.rq` discovered as render
inputs. Legacy gate-as-query behavior survives ONLY behind a legacy profile
(§86 step 6, §89) — default for NEW packs is refusal semantics.

## Scope

1. Find pack loading (grep `gates` under `lib/`). Add refusal execution for
   `gates/*.rq` before render; add `queries/*.rq` as the render-binding
   source (the role gates play today).
2. Profile switch: default (portable) = new semantics; legacy profile =
   today's behavior unchanged. The switch mechanism should match how the
   repo already configures engines/profiles if such a mechanism exists,
   else a module attribute / config key — record the choice.
3. Gate evidence (§15): each gate result records gate identity, violation
   rows/ASK value, decision — at minimum in the refusal error/log payload.
4. Tests (the D1 pair, mirrored from Rust T06):
   - queries/ SELECT with rows → renders, no refusal.
   - gates/ same SELECT → sync refuses BEFORE any file write (assert no
     target file exists after the refused run — that ordering IS the test).
   - Legacy profile still renders from gates/ (compat witness).
5. Gate sabotage (§79): invert one test to prove it can fail; note it.

## Acceptance

Real `mix test` (changed-scope files) exit 0 + the three witnesses in
History with real exit codes.

## Out of scope

Renderer identity (T15), pack.toml (T13), canonical bindings (T14),
reconciliation changes.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:09Z | UNKNOWN | gpack/ign-12-gate-semantics@15305cea | orient: ticket + RFC §14/§15/§16/§79/§86(3,5,6)/§89 + D1 read; AGENTS.md+CLAUDE.md read; conflation located: `Pack.discover_queries/1` globs `gates/*.rq` as render queries, consumed by reconcile.ex:243, sync.ex:1326 (reactor path via `resolve_named_queries!/2`); measured: 0 of 12 `priv/ggen` packs have `queries/` (all legacy-shaped, §89) | profile mechanism decision, refusal gates, D1 tests |
