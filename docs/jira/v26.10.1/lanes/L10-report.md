# L10 report — skeptic seam recomputation

- lane: L10
- branch: `release/v26.10.1` @ `19a2b1f1` (verified first action; base `dc665a1e`)
- files-written:
  - `docs/releases/v26.10.1-seam-audit.md` (new, UNSTAGED)
  - `docs/jira/v26.10.1/lanes/L10-report.md` (this file)
- no other file touched; RESOLUTIONS.md untouched; no git state commands run

## Decisions + rationale

1. Recomputed all seams network-first (`ls-remote`, `gh`), not from RESOLUTIONS text, per skeptic mandate.
2. Verdict: `AUDIT: 19 seams checked, 15 MATCH, 4 MISMATCH, 0 UNKNOWN` → `REFUSED_SEAM_CONFLICT` with 4 items, all statement/citation-level inside RESOLUTIONS.md:
   - MC-1: ggen `v26.10.0` GitHub release EXISTS (0 assets, published 2026-07-20, not draft) vs expected "NOT FOUND". Materially consistent with the L1 decision (no assets; latest asset-bearing release still `v26.9.28`); wording in RESOLUTIONS imprecise. Not remote movement (predates computation).
   - MC-2: lock `[container]` precedent tag cited as `v26.9.25`, observed `v26.9.29` (pattern BLOCKED + requires_republish=true matches exactly; lock untouched by L1, so HEAD authoritative).
   - MC-3: ontology.ttl + sync.yml from-side tag cited `v26.9.25`; HEAD = `v26.9.29` (workflow lines 11/38, ontology 25/52). `v26.9.25` exists only in `archive/pre-v26.10.1-dirty-20261001`. L4 must bump from `v26.9.29` or a literal replace finds nothing. To-side `v26.10.1` unaffected.
   - MC-4: from-side `marketplace_sha` cited `2c4c4c7e...`; HEAD = `637b561c...` (= lock `latest_published_release_sha`). `2c4c4c7e` exists only in archive. To-side `bf9eccb3...` is network-verified (vendor main head) and already the value in lock `[ggen_marketplace].sha`/`[pragprog_tps].marketplace_sha`/`[submodules].ggen_marketplace_commit` at HEAD.
3. Clean results worth recording: all 6 crown targets reproduced live (12/12 symref + explicit-ref checks, zero staleness); all 5 RESOLUTIONS `describe` claims reproduced exactly; v26.10.1 tag absent in all 3 remotes (new identity confirmed); HEAD vendor gitlinks already = crown targets (older pins live in the archive ref AND the working-tree checkouts — crown-at-integration moves worktree, committed side already target-valued; RESOLUTIONS' "pre-bump pins live in HEAD" phrasing noted as misleading, observation only).
4. Derived-pin method spot-checks resolve at pinned SHAs: ggen_igniter `mix.exs` @ `0abed8a3` → `version: "26.9.30"`; wasm4pm `Cargo.toml` @ `a7352d81` → `version = "26.9.30"` (both differ from HEAD lock's `26.9.29`/`26.9.28`, corroborating the read-never-guess instruction).

## Commands + exits

| command | exit | result |
|---|---|---|
| `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 | `release/v26.10.1` / `19a2b1f1` |
| `git ls-remote origin main` | 0 | `dc665a1e...` MATCH |
| `git -C vendor/<v> ls-remote --symref origin HEAD` ×6 | 0 | all 6 default branches + heads MATCH |
| `git -C vendor/<v> ls-remote origin <default>` ×6 | 0 | all 6 head SHAs MATCH |
| `gh release view v26.9.28 -R seanchatmangpt/ggen --json tagName,publishedAt,assets ...` | 0 | 2026-09-29T02:21:02Z, 12 assets incl. linux x86_64 + darwin aarch64 — MATCH |
| `gh release view v26.10.0 -R seanchatmangpt/ggen 2>&1 \| head -1` | 0 | `title: v26.10.0` — expected NOT FOUND — **MISMATCH MC-1** |
| `gh release view v26.10.0 -R seanchatmangpt/ggen --json tagName,publishedAt,isDraft,isPrerelease,assets ...` | 0 | assetCount=0, publishedAt=2026-07-20T18:41:25Z, isDraft=false |
| `gh release view -R seanchatmangpt/ggen --json tagName,publishedAt ...` (latest) | 0 | `v26.9.28` @ 2026-09-29 — confirms L1 decision basis |
| `git -C vendor/ggen ls-remote origin refs/tags/v26.10.0` | 0 | `82795cda...` MATCH |
| `git ls-remote --tags origin \| grep -c v26.10.1` (ggen-ecosystem, vendor/ggen, vendor/ggen-marketplace) | 0 (grep exit 1 ×3) | 0/0/0 MATCH |
| `git show HEAD:ecosystem.lock.toml` `[container]` | 0 | tag `v26.9.29` + BLOCKED + requires_republish=true — pattern MATCH, tag **MISMATCH MC-2** |
| `git show HEAD:{ontology.ttl,.github/workflows/ggen-ecosystem-sync.yml} \| grep default:` / same on archive ref | 0 | HEAD `v26.9.29`/`637b561c...`; archive `v26.9.25`/`2c4c4c7e...` — **MISMATCH MC-3/MC-4** |
| `git show HEAD:ecosystem.ttl \| grep hasVersion` | 0 | `"26.8.27"` at HEAD — MATCH |
| `git ls-tree dc665a1e/HEAD/archive vendor/` | 0 | HEAD+base = 6 crown targets; archive = 6 older WIP SHAs |
| `git describe --tags <sha>` ×6 in vendor repos | 0 | all 5 RESOLUTIONS describe claims reproduced + autofde recorded |
| `git -C vendor/ggen_igniter show 0abed8a3:mix.exs \| grep 'version:'` | 0 | `26.9.30` |
| `git -C vendor/wasm4pm show a7352d81:Cargo.toml \| grep '^version'` | 0 | `26.9.30` |
| `git status --short`, `git log --oneline dc665a1e..HEAD`, `git diff dc665a1e HEAD -- vendor/` (read-only) | 0 | 1 scaffolding commit; zero gitlink delta base..HEAD; lock unmodified |

## REFUSED / BLOCKED / UNKNOWN items

- `REFUSED_SEAM_CONFLICT` ×4: MC-1 (v26.10.0 release existence vs "NOT FOUND"), MC-2 (container precedent tag `v26.9.25` vs observed `v26.9.29`), MC-3 (from-side tag `v26.9.25` vs HEAD `v26.9.29`), MC-4 (from-side `marketplace_sha` `2c4c4c7e` vs HEAD `637b561c`). Both values + both source commands recorded per item in `docs/releases/v26.10.1-seam-audit.md`. RESOLUTIONS.md not edited, per lane law.
- No BLOCKED. No UNKNOWN (every seam resolved to an observed value; vendor objects for derived-pin checks resolved locally at the pinned SHAs).
