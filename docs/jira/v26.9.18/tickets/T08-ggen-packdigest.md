# T08 — ggen: portable SHA-256 PackDigest (§38 ggen-pack-v1)

- Repo: `seanchatmangpt/ggen` (worktree: `~/wt-v26918/ggen-08-packdigest`)
- Branch: `gpack/ggen-08-packdigest` (pre-created off `origin/main` = `ad3a7e661`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§37, §38, §39, §96, §72)

## Goal

RFC §85 step 8: SHA-256 PackDigest computed IN ADDITION to the existing
BLAKE3 content hash (nothing replaced). Algorithm is normative (§38) —
implement it exactly; cross-engine digest equality (Appendix E row 1)
depends on byte-exactness.

## Scope

1. `PackDigest = SHA256( "ggen-pack-v1\0" ∥ E1 ∥ … ∥ En )` where
   `Ei = u64be(|path_i|) ∥ path_i ∥ u64be(|bytes_i|) ∥ bytes_i`, files sorted
   by UTF-8 path bytes, path = normalized relative path, symlinks excluded
   from canonical source → `REFUSED:PACK_SYMLINK` (§72) rather than hashed.
2. Digest scope = §39 (pack.toml, RDF, queries, gates, rules, templates,
   hook declarations, pack-owned qualification contracts; never caches or
   emitted consequences). If the existing hash has a scope list, mirror it.
3. Expose in sync output (existing hash output shape + `pack_digest_sha256`)
   and in lock/receipt structures where the BLAKE3 already appears — additive
   fields only.
4. Tests:
   - Known-vector: hand-compute the digest for a 2-file fixture in the test
     (construct the byte string in the test, sha256 it, compare).
   - §96 digest-completeness falsifier: modify a gate file → digest changes;
     touch mtime only (no byte change) → digest IDENTICAL (§38 meta-law).
   - Symlink in pack source → typed refusal (create it in a tempdir at test
     runtime, never in git).

## Acceptance

Real `cargo test` (changed scope) exit 0 + the three falsifiers above run
(including the inverted-run witness for at least the completeness test).

## Out of scope

Igniter's digest (wave 2 crown compares); replacing BLAKE3; archive digests
(§40 stays separate).

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|

## RESCOPE (2026-09-18T06:35Z, after T10 merged as ggen PR #715)

T10 delivered the §38 `pack_digest_sha256` (known-vectors, envelope binding) on
ggen main. This ticket's remaining unique scope:

1. §72: symlink inside pack source → `REFUSED:PACK_SYMLINK` (T10 recorded the
   digest walk does NOT refuse symlinks yet).
2. Coordination: confirm the digest file set and the T10 envelope agree after
   T07's `.tera` discovery lands (`.tera` files must be in-scope for the
   digest; add a test proving a `.tera` byte change moves the digest once T07
   is in).
3. Cross-check: run T10's `portable_receipt_e2e` alongside the new symlink
   falsifier; both suites green.

Original known-vector/completeness work: already delivered by T10; do not
duplicate. History rows continue here.
