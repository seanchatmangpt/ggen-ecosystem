# T09 — ggen: consumer alias ≠ canonical pack name (§9)

- Repo: `seanchatmangpt/ggen` (worktree: `~/wt-v26918/ggen-09-alias`)
- Branch: `gpack/ggen-09-alias` (pre-created off `origin/main` = `ad3a7e661`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§9, §96)

## Goal

RFC §85 step 9: distinguish canonical pack name (from pack.toml) from the
consumer's local alias (the `[packs]` key). The alias MUST NOT overwrite
canonical identity in receipts or dependency resolution.

## Scope

1. Resolution keeps both: `consumer_alias` (config key) and `canonical_name`
   (parsed from the pack's pack.toml `[pack].name`).
2. Receipts/lock entries record BOTH fields (additive; existing fields keep
   meaning — where today only the alias appears, add canonical_name beside
   it rather than renaming).
3. §8 correspondence is admission's business, NOT aliasing: an alias may
   differ from canonical name lawfully (that is its purpose).
4. Tests:
   - `consumer_alias_preserved`: pack dir name/canonical `acme-payments-pack`
     aliased as `payments` in ggen.toml → sync receipt/output shows both,
     canonical wins in identity fields.
   - Inversion witness: assert that removing the alias distinction would
     fail — i.e. the test fails if canonical_name is ever written as the
     alias (construct the assertion so a conflated implementation cannot
     pass).
5. Existing suites green (compatibility falsifier recorded).

## Acceptance

Real `cargo test` (changed scope) exit 0 + both falsifiers + the untouched
legacy run in History.

## Out of scope

Marketplace `directory_name == canonical_name` strictness (§9 is marketplace
admission, not local composition); dependency resolution semantics (§26+ is
a later ladder — this ticket only records identities correctly).

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
