# T07 — ggen: .tera discovery + explicit renderer identity (D2)

- Repo: `seanchatmangpt/ggen` (worktree: `~/wt-v26918/ggen-07-tera-renderer`)
- Branch: `gpack/ggen-07-tera-renderer` (pre-created off `origin/main` = `ad3a7e661`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md` (§17–§22, §96, D2)

## Goal

RFC §85 steps 6+7: explicit renderer metadata + `.tera` portable discovery,
with `.tmpl` legacy profile byte-identical (§85 step 2, §21, §88).

## Scope

1. Template discovery additionally accepts `templates/**/*.tera`, rendered
   with the existing Tera engine.
2. Frontmatter MAY carry `renderer:` (normalized §22 contract: `tera1` is
   the only value this change accepts). Rules:
   - `.tera` + `renderer: tera1` → render.
   - `.tera` + unknown renderer value → `REFUSED:RENDERER_AMBIGUOUS` (typed,
     §100: no silent fallback).
   - `.tmpl` behavior unchanged in every case (legacy profile, §88).
3. A pack mixing `.tmpl` and `.tera` is lawful; both render.
4. Tests:
   - `.tera` pack renders end-to-end (positive).
   - `.tera` + `renderer: eex1` → typed refusal naming
     `UNSUPPORTED:RENDERER:EEx1` or `REFUSED:RENDERER_PROFILE_MISMATCH`
     (§19 wording; pick the existing error style, record choice).
   - Existing `.tmpl` suite untouched and green (the compatibility
     falsifier — state the command that proves it).

## Acceptance

Real `cargo test` (changed-crate scope) exit 0 + the three-way evidence
above in History.

## Out of scope

EEx implementation (UNSUPPORTED classification is the correct Rust answer);
frontmatter schema versioning beyond `renderer:`; Igniter.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
