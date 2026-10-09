# R59 — ecosystem.lock.toml Standing Drift (STALE)

Date: 2026-10-09
Lane: R59 (campaign receipt standing, v26.10.8 semantic wave)
Subject: `/Users/sac/ggen-ecosystem` @ 9831528e (main)

## Standing

`STALE` — all six `[submodules]`/vendor rows in `ecosystem.lock.toml`
(updated_at 2026-10-01T20:47:35Z) trail the campaign's landed state as of
2026-10-09. This note records the drift only. Per C04/C15 doctrine, the lock
file is NOT rewritten here: lock/crown transitions are coordinator/operator-
gated (C15 authority-closure invalidation; lock standing bound to fcd6a068-era
receipts). No lock edit is included in this commit.

## Drift table (old → new, real SHAs)

| row | lock (old) | landed (new) | landed ref | evidence |
|---|---|---|---|---|
| ggen | `ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e` | `5cae792fccc796c1a4769461dc2eb39388391058` | origin/spec-integration | `git -C ~/ggen rev-parse HEAD`; commit "docs(sjira): R35 — pre-push hook ref-validation fix + main patch landing" |
| ggen-marketplace | `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2` | `f4b8b4fc46a3acd2675a31e3ffd9dabf7032ed31` | origin/main | `git -C ~/ggen-marketplace rev-parse HEAD`; commit "fix(scripts): pyright Optional/union defects … (R50)" |
| ggen_igniter | `0abed8a35db68c18bba6982b266dd7546c162d1c` | `c8846c728ce9dce07e9835b3aeb2931b4264ff1e` | origin/main | `git -C ~/ggen_igniter rev-parse HEAD` |
| beam4pm | `c3017e4283777927eb01b5049bfa8b07d4e6ac7b` | `eb07f235d650a0b9fa3cea3be5a0181854cdc472` | origin/main | `git -C ~/beam4pm rev-parse HEAD` |
| wasm4pm | `a7352d818dbcaa15909833f13ac367dc5950a7a9` | `2bb0c4ecfa56b237e0db860616b9e71f87a01a14` | origin/main | `git -C ~/wasm4pm rev-parse HEAD` (branch docs/doc-hdit-scaffold-w4p, contained in origin/main) |
| autofde-lab | `71de04a60db723764fab5afe042b42937b471e0e` | `fbd6eab4525d63516c5377e811ac1b92ab4c15f8` | origin/lane/doc-hdit-scaffold | `git -C ~/autofde-lab rev-parse HEAD` |

Verification method: `git submodule status` in this repo matches the lock
exactly (internally consistent, externally stale); each canonical checkout's
HEAD confirmed with `rev-parse` and containment via `branch -r --contains HEAD`.
None of the landed SHAs exist as objects in this repo's vendor checkouts
(`cat-file -t` fails for 5cae792fc / f4b8b4fc4) — vendor trees not yet fetched
forward.

## Justifying receipts per row

- ggen 5cae792fc: R35 sjira pre-push hook ref-validation fix (commit subject
  names the lane receipt; campaign SEMANTIC-WAVE / TAG-STANDING landed state).
- ggen-marketplace f4b8b4fc4: R50 pyright defect fixes in
  es_chain_qualify/entitlement/pack_capabilities/regen_solution_lock/
  workflow_census (campaign receipt chain lives in ggen-marketplace).
- ggen_igniter c8846c72, beam4pm eb07f235, wasm4pm 2bb0c4ec, autofde-lab
  fbd6eab4: doc-hdit scaffold wave landings on their respective remotes
  (BRANCH-CENSUS landed state). Per-row detailed receipts live in those repos'
  docs/sjira lanes.

## Other standing artifacts observed

- No `CAMPAIGN-RECEIPT` file present in this repo.
- Governor demand store: 43 open issues on
  seanchatmangpt/ggen-ecosystem (read via `gh issue list --state open`,
  2026-10-09).
- `docs/sjira/v26.10.8/` contains only `WORKGRAPH.ttl` prior to this note.

## Falsifier / replay

Re-run: `git submodule status` + the rev-parse commands in the drift table.
If vendor submodules are fetched forward and the lock rows move to the new
SHAs with receipts, this note is retired. Until then the lock's
`updated_at = 2026-10-01T20:47:35Z` marks its observation horizon.
