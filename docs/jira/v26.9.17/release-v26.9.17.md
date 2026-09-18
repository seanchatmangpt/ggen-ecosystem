# Release v26.9.17 — RFC-GPACK-001 landing + ecosystem release identity

Operator instruction (verbatim): `finish, validate, benchmark, then tag v26.9.17`.

## Scope

1. Land RFC-GPACK-001 v26.9.17 (GGEN Semantic Pack Protocol) as
   `docs/RFC-GPACK-001-v26.9.17.md` — operator-supplied draft, grounded against the
   exact producer heads already pinned in `ecosystem.lock.toml`
   (ggen `ad3a7e661`, ggen-marketplace `800b8c6c5`, ggen_igniter `15305cea`).
2. Capture this milestone's session records (cleanup-merge-plan.md + this ticket).
3. Fix the recurring `ggen.toml` `[packs]`-comment-vs-pin drift (class
   #248/#263/#266/#267) **and** encode a permanent lock-contracts tripwire so the
   same drift cannot silently recur — the falsifier for the drift class.
4. Bump release identity `v26.9.10` -> `v26.9.17` (`[ggen].release` +
   `[container].tag`), CHANGELOG entry, merge, annotated tag `v26.9.17` on the
   inspected merge head. Tag push triggers `ggen-ecosystem-container.yml`, whose
   fresh build is the path to clearing the known `[container] standing = BLOCKED /
   requires_republish` state (per v26.9.10 precedent, `[container]` digest/standing
   are updated in a follow-up only after the real build succeeds — never fabricated).

## Non-goals

- `ggen-pack-spec-pack` + first cross-engine portable fixture (RFC's recommended
  first implementation artifact) — marketplace-side implementation work, next
  ticket, not this release.
- The sync workflow's generated `ggen_container_tag` default (`v26.8.28`) —
  generated projection; callers pass explicit tags; repair belongs in the owning
  pack if wanted.
- The cleanup plan's Still Open deletion pass (branches/worktrees) and the
  `docs/capture-v26.9.15-review-and-crown-receipt` PR decision — explicitly left
  for the operator.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-17T21:05Z | PARTIAL_ALIVE | release/v26.9.17 @ (pre-commit) off origin/main 30183b07 | submodules synced to gitlinks (6/6 match lock); RFC extracted verbatim (2889 lines) | docs commit, ggen.toml fix + tripwire, release bump, validate, bench, merge+tag |
