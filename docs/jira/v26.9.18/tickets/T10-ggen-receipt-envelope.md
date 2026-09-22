# T10 — ggen: portable receipt envelope v1 (§54/§55)

- Repo: `seanchatmangpt/ggen` (worktree: `~/wt-v26918/ggen-10-receipt-envelope`)
- Branch: `gpack/ggen-10-receipt-envelope` (pre-created off `origin/main` = `ad3a7e661`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§54, §55, §56, §57)

## Goal

RFC §85 step 12: emit the portable receipt envelope alongside existing
receipts (§56: Rust BLAKE3 chains continue; envelope must not claim
byte-equivalence).

## Scope

1. New output path (e.g. `--receipt-format portable` or an additive field on
   the existing JSON receipt — match repo idioms, your call, recorded):
   the §55 shape with EVERY §54 field present:
   `schema="https://ggen.dev/receipt/pack/v1"`, `spec="RFC-GPACK-001-v26.9.17"`,
   engine{name,version}, subject{pack,version,pack_digest}, dependencies[]
   {name,version,digest,scope[]}, graph{canonical_digest},
   admission{gates_attempted[],refusals[]}, consequences[]
   {target,operation,sha256}, replay{status}, standing.
2. `standing` uses §82 vocabulary only; a refused sync emits the envelope
   with typed `REFUSED:<CODE>` in admission.refusals and standing REFUSED
   (§57: the envelope existing is not standing — it REPORTS standing).
3. Fields this run cannot know (e.g. replay not yet executed) are present
   with `status:"UNKNOWN"` — no omission, no invention (§54 "binds at least").
4. Tests:
   - Happy-path sync → envelope parses as JSON, all keys present (schema
     -validate the field set, not just parse).
   - Gate-refused sync → envelope contains the typed refusal and standing
     REFUSED (the §57 falsifier: receipt exists AND reports refusal).
   - pack_digest in envelope == T08's SHA-256 digest for the same pack
     (cross-field identity witness; coordinate by computing both in the test).

## Acceptance

Real `cargo test` (changed scope) exit 0 + the three witnesses in History.

## Out of scope

Igniter envelope; replay execution (status stays UNKNOWN unless the repo
already replays); receipt schema registry.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:31:32Z | PARTIAL_ALIVE | gpack/ggen-10-receipt-envelope@16c53a3ad (base ad3a7e661, 1 commit, not pushed) | `cargo check -p ggen-engine` exit 0; `cargo test -p ggen-engine --lib` exit 0 (198 passed, 2 pre-existing ignored) incl. §38 known-vector digest tests; `cargo test -p ggen-engine --test portable_receipt_e2e` exit 0 (5 passed) | none blocking; clippy/fmt clean on touched files; legacy regressions being run |
| 2026-09-18T06:31:32Z | ALIVE | gpack/ggen-10-receipt-envelope@16c53a3ad | Full changed-scope evidence, all exit 0: `cargo test -p ggen-engine --lib` (198 passed) — §38 vector 00d88d57…ee1cc + 87a71f12…a54a + .git-exclusion guard; `portable_receipt_e2e` 5/5 — W1 happy-path §54 field-set schema check (schema/spec/engine/subject/dependencies/graph/admission/consequences/replay/standing, consequence sha256 re-hashed off disk, legacy BLAKE3 receipt §56 witness), W2 §57 falsifier (gate-refused sync → envelope exists AND reports `REFUSED:GATE_VIOLATION` + `FM-PACK-013`, zero consequences, target unwritten), W3 pack_digest == independent in-test §38 computation, != BLAKE3 chain hash; `pack_e2e` 15/15, `receipt_chain_e2e` 16/16, `sync_e2e` 11/11, `sync_dry_run_no_mutation_e2e` 1/1, `write_stage_partial_failure_receipt_binding` 1/1, `migration_receipt_persist` 1/1, `receipt_epoch_e2e` 12/12 (legacy behavior preserved; pack_e2e requires pre-built `ggen` bin from ggen-cli-lib — without it 3 tests fail on unset `CARGO_BIN_EXE_ggen`, verified identical on pristine base ad3a7e661, pre-existing environmental edge, not this change) | Recorded edges (silent pruning = none, all disclosed): multi-pack syncs report the lexicographically-first pack as envelope subject (per-pack envelopes deferred to §85 steps 10–11 dependency tickets); `dependencies[]` present and always empty (Rust packs have no declared dependency surface yet — steps 10–11 own it); §9 consumer-alias vs canonical name not separated (step 9's ticket; envelope carries the `[packs]` resolution key the engine resolves); refusal envelopes cover the 4 gate-stage sites only — `[law].shapes`/`shapes.ttl` migration refusals, denial refusals ([FM-LAW-011]) and pre-admission failures do not emit (existing typed errors unchanged); declarative-rules `[[generation.rules]]` path and dry runs emit nothing (zero-side-effect contract); §72 symlink refusal not added to the digest walk (mirrors `content_hash` file set; admission tickets own it); `replay.status` always UNKNOWN (out of scope per ticket) |
