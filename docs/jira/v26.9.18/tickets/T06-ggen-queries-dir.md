# T06 — ggen: queries/ discovery distinct from gates/ (D1)

- Repo: `seanchatmangpt/ggen` (worktree: `~/wt-v26918/ggen-06-queries-dir`)
- Branch: `gpack/ggen-06-queries-dir` (pre-created off `origin/main` = `ad3a7e661`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§13, §14, §96, D1)

## Goal

RFC §85 step 4: "add explicit queries/" while preserving current gate
semantics (§85 step 3). Rust ggen today reads `gates/*.rq` as refusal law.
Add `queries/*.rq` as NAMED QUERIES with retrieval semantics — results
available as render bindings, NEVER interpreted as refusals.

## Scope

1. Find the gate discovery/execution code (grep `gates` under `crates/`).
   Add a parallel `queries/` discovery: same .rq parsing, but results are
   exposed as named bindings for templates; a query returning rows causes
   NO refusal and NO error.
2. §13 canonical order: discover both dirs in sorted lexical path order.
3. Tests (the §96 falsifier pair — these two tests are the heart of D1):
   - `query_positive_select_does_not_refuse`: pack with a SELECT returning
     ≥1 row in `queries/` → sync succeeds.
   - `gate_positive_select_refuses`: the SAME query in `gates/` → sync
     refuses with the gate-violation error path.
4. Existing gate tests stay green, byte-identical behavior.

## Acceptance

`cargo test` (narrowest scope covering the changed crate + the two new
tests) real exit 0 in History. The two new tests must BOTH exist and pass;
deleting either must make the suite fail (state how you know — e.g. run
once with the test's assertion inverted to see it fire, then restore).

## Out of scope

Igniter; renderer identity (T07); dependency semantics; portable digest.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:00:50Z | UNKNOWN | gpack/ggen-06-queries-dir@ad3a7e661 (clean) | orient: ticket+RFC §13/§14/§85/§96/D1 read; gate code located `crates/ggen-engine/src/sync.rs` (`list_gate_files`, `evaluate_gate`, pack loop ~L691); worktree AGENTS.md read | implement queries/ discovery + bindings; falsifier pair; cargo test -p ggen-engine; commits |
| 2026-09-18T06:24:45Z | PARTIAL_ALIVE | gpack/ggen-06-queries-dir@ad3a7e661 + working tree (sync.rs +128/-22, tests/pack_queries_dir_e2e.rs new) | `cargo check -p ggen-engine` exit 0; `cargo test -p ggen-engine --test pack_queries_dir_e2e` exit 0 (2 passed) with `CARGO_BIN_EXE_ggen=$PWD/target/debug/ggen`; falsifier-inversion run exit 1 (both inversions fired: query test saw exit 0, gate test saw exit 1), assertions restored | incident: careless `rm -f` deleted uncommitted sync.rs mid-session; recovered via `git checkout --` + re-apply of all 6 edits (all in session transcript); diff stat verified 128/-22. FINDING: `CliHarness::cargo_bin` falls back to PATH when CARGO_BIN_EXE_ggen unset → without the env var the e2e tests run the INSTALLED ggen 26.8.18, not the workspace build (observed: query test failed with FM-TPL-017 against installed binary). All gates+exits below pin the env var to the workspace binary | run full `cargo test -p ggen-engine` (env-pinned); existing gate tests byte-identical; commit |
