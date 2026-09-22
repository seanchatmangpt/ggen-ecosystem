# T13 — ggen_igniter: pack.toml consumed + identity correspondence (D3, §8)

- Repo: `seanchatmangpt/ggen_igniter` (worktree: `~/wt-v26918/ign-13-manifest`)
- Branch: `gpack/ign-13-manifest` (pre-created off `origin/main` = `15305cea`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§7, §8, §86 steps 1+2, D3)

## Goal

Resolve D3: Igniter today does not read pack.toml during pack resolution.
For packs declaring the Core profile (gp:profile gp:Core1 or Portable1 in
their graph), pack.toml becomes REQUIRED and its identity must correspond
with the graph: `Project(I_S) = I_B` (§8) — mismatch ⇒
`REFUSED:PACK_IDENTITY_MISMATCH`. Legacy packs (no profile declaration)
keep today's optional-manifest behavior (§86 step 2, §89).

## Scope

1. Parse pack.toml when present: strict §7.1 `[pack]` (name, version,
   description; unknown keys inside [pack] ⇒ `REFUSED:PACK_MANIFEST_INVALID`
   for Core-profile packs).
2. Correspondence: graph `gp:name` (if declared) == manifest name for
   Core-profile packs; graph declares no gp:name + manifest present ⇒
   correspondence fails closed for Core profile (the RFC requires the
   projection relation to hold when the graph declares identity; a Core
   pack SHOULD self-describe, §10 — treat missing as mismatch, recorded).
3. Legacy detection: no `gp:profile` in graph ⇒ legacy path, manifest
   optional, zero new refusals (byte-compat).
4. Tests:
   - Core pack, matching identities → admitted.
   - Core pack, manifest name ≠ gp:name → REFUSED:PACK_IDENTITY_MISMATCH.
   - Core pack, unknown [pack] key → REFUSED:PACK_MANIFEST_INVALID.
   - Legacy pack without pack.toml → unchanged behavior (compat witness).
   - Inversion witness on the mismatch test (prove it can fail).

## Acceptance

Real `mix test` (changed scope) exit 0 + all five witnesses in History.

## Out of scope

Rust manifest handling; dependency/version fields (§26+ later ladder);
renderer/marketplace manifests.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:04:10Z | UNKNOWN | gpack/ign-13-manifest@15305ce (clean, = origin/main) | ticket+RFC read; worktree clean; `mix deps.get` exit 0; no tests run yet | implement pack.toml parse (§7.1) + gp:profile detection + identity correspondence (§8); wire into ReconcileReactor pack-resolution path; 5 witnesses + mix test |
| 2026-09-18T06:10:00Z | PARTIAL_ALIVE | gpack/ign-13-manifest@15305ce | design settled: `GgenIgniter.Pack.Manifest` struct + `Pack.parse_manifest/1` + `Pack.declared_profile/1` + `Pack.admit_pack_manifest/2` (RFC §7.1, §8, §10, §12.1, §86.1-2, §89, App. C); enforcement seam = new `:admit_pack` step in `ReconcileReactor` (single dispatch path of `sync`, pre-`:run_queries` dependency edge) + `ReconcileReactor.plan/1`; refused-step standing map updated; tests planned as tmp-dir Chicago fixtures + pipeline-level run/1 + plan/1 witnesses; legacy = no gp:profile ⇒ :ok pass-through (zero new refusals) | write code, write tests, run mix test |
| 2026-09-18T06:33:29Z | ALIVE | gpack/ign-13-manifest@0f34070 (1 commit on 15305ce, tree clean, not pushed) | `mix compile` exit 0 (no warnings). `mix test test/ggen_igniter_pack_manifest_admission_test.exs` exit 0 — 25 tests/0 failures. `mix test test/ggen_igniter_reconcile_reactor_test.exs test/ggen_igniter_pack_test.exs test/ggen_igniter_sync_pack_test.exs test/ggen_igniter_pack_discovery_matrix_test.exs test/ggen_igniter_plan_task_test.exs test/ggen_igniter_plan_schema_test.exs` exit 0 — 98/0. `mix test test/ggen_igniter_sync_task_test.exs test/ggen_igniter_sync_for_each_reactor_test.exs test/ggen_igniter_sync_inject_reactor_admission_test.exs test/ggen_igniter_sync_inprocess_reconcile_test.exs test/ggen_igniter_sync_dry_run_test.exs test/ggen_igniter_reconcile_reactor_inject_test.exs test/ggen_igniter_sync_inject_test.exs` exit 0 — 29/0. `mix test ...stale_delete... ...compensation_failure... ...pack_properties... ...sync_frontmatter...` exit 0 — 3 properties + 5 tests/0. Post-format consolidated `mix test admission+pack+reactor+discovery` exit 0 — 108/0. FIVE WITNESSES OBSERVED: (1) Core match admitted (`:ok` unit + `run/1` end-to-end `standing: :alive`, real file written); (2) Core manifest name ≠ gp:name ⇒ `{:refused, {:pack_identity_mismatch, ...}}` incl. real `run/1` receipt `standing: :refused`, reason `REFUSED:PACK_IDENTITY_MISMATCH`, zero files written; (3) unknown `[pack]` key (`homepage:`) ⇒ `{:refused, {:pack_manifest_invalid, ...}}`; (4) legacy pack without pack.toml ⇒ `:ok` unchanged (tmp legacy pack + real `test/fixtures/sample-pack` compat witness, unit + `plan/1` pipeline); (5) §79 inversion witness — deleting ONLY the `gp:profile` fact (same gp:name, same pack.toml) flips the refused subject to `:ok` and `parse_manifest` alone succeeds ⇒ guard is load-bearing, not vacuous. Extra normative witnesses: Core pack missing pack.toml ⇒ REFUSED:PACK_MANIFEST_MISSING; Core graph with no gp:name ⇒ mismatch fail-closed; second disagreeing gp:name ⇒ refuse (no silent first-match); Dataset/quad profile detection; invalid-TOML via real broken-pack fixture. FILES: lib/ggen_igniter/pack.ex, lib/ggen_igniter/pack/manifest.ex (new), lib/ggen_igniter/reactors/reconcile_reactor.ex, test/ggen_igniter_pack_manifest_admission_test.exs (new). Operator wrote 0 of the 924 inserted lines. RECORDED EDGES (no silent pruning): (a) unknown keys OUTSIDE `[pack]` not refused — §7.1's MUST covers only keys inside `[pack]`; (b) an unknown gp:profile (≠Core1/Portable1) classifies :legacy — no Core enforcement, no Core privileges; §100 UNSUPPORTED is a later ladder; (c) enforcement wired at ReconcileReactor (run/1 + plan/1) = the only `sync` dispatch path; standalone `GgenIgniter.Reconcile.run/1` (reachable only via the retired Controller path) and read-only `doctor` NOT wired — deliberate; (d) on the `--for-each` path the task pre-loads driver rows before the reactor's `:admit_pack`, but refusal still precedes ALL actuation (reactor-owned), fail-closed holds; (e) gp:version correspondence NOT enforced — ticket out-of-scope (§26+ later ladder); (f) out-of-scope per ticket: Rust manifest handling, renderer/marketplace manifests | none — ticket scope complete; T13 done |
