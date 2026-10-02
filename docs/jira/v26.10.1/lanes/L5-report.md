# L5 report — current release standing → v26.10.1

- lane: L5
- date: 2026-10-01
- branch at start (and end): `release/v26.10.1` @ `19a2b1f1` (base `dc665a1e93573949040900faa65b46af3a3ea6d9` = origin/main)
- files-written (left UNSTAGED, no git add):
  - `docs/CURRENT-RELEASE-STANDING.md` (modified in place on top of the preserved v26.9.25/26-era WIP corrections; WIP intent preserved and demoted to labeled history, not reverted)
  - `docs/jira/v26.10.1/lanes/L5-report.md` (this file)

## Decisions + rationale

1. **Subject block replaced with the v26.10.1 crown seams, every value independently verified before writing** (commands below). Contract-supplied grep `grep -m1 '^version'` on `vendor/ggen_igniter` mix.exs returned empty because the version line is indented (`      version: "26.9.30"`); re-verified with `grep -in version` → `version: "26.9.30"` at mix.exs line 9, matching lock `[ggen_igniter].version`. Not a seam conflict.
2. **Capsule standing = `BLOCKED[AWAITING_PUBLISH]` for tag `v26.10.1`**, stated exactly as the lock records it (`[container]` `standing = "BLOCKED"`, `requires_republish = true`, failure line "v26.10.1 image not yet published... awaiting the ggen-ecosystem-container build and independent pull verification"). No execution evidence claimed; the crown lands at integration.
3. **Wording-accuracy note (not a seam conflict): the contract phrase "the v26.9.29-era image is superseded and awaits republish" is not what the evidence shows.** There was never a published v26.9.29-era image: the pre-bump (HEAD) lock `[container]` records tag `v26.9.29` with `requires_republish = true` and failure "v26.9.29 image not yet published"; the digest on record (`sha256:6605878e...`) was introduced by `327fd84c` (2026-09-23, "receipts(release): v26.9.22 container published and verified") — i.e. the v26.9.22-era image, observed run `35833887166` @ head `97620bdd`. The doc therefore says: v26.9.25 and v26.9.29 crowns each recorded `BLOCKED[AWAITING_PUBLISH]` against that same v26.9.22-era digest and were superseded without a publish. The seam itself (`BLOCKED[AWAITING_PUBLISH]` for v26.10.1) is fully supported by evidence; seam left unchanged, phrasing made exact.
4. **Preserved WIP corrections treated as history per dispatch note (v26.9.25→v26.9.29 = HISTORY, v26.10.1 = current).** The v26.9.25-era lead paragraph was rewritten into the v26.10.1 lead plus a one-paragraph "History:" note; the 2026-08-29 GHCR root-cause paragraph and the ALIVE-era re-verification (digest `b9e17023...`, `ggen 26.8.28`) were kept byte-for-byte with an added "Historical (2026-08-29, ALIVE era)" label (the old "the **same** digest" anaphora would have dangled after the lead changed). Lock correspondence section and Promotion falsifier section left untouched — already historical/structural, and the preamble labels the DoD rows as historical evidence.
5. **v26.10.0 zero-asset fact cited, not re-witnessed:** tag existence verified locally (`git -C vendor/ggen rev-parse v26.10.0^{commit}` → `82795cda...`); the zero-asset release-object property is taken from RESOLUTIONS.md's decision record and is consistent with lock `[ggen]` (`release = "v26.9.28"`, `upstream_release = "v26.9.28"`, L1's option (a)). No GitHub API fetch performed in this lane.
6. **Sweep result:** post-write `grep -nE 'v26\.[0-9]|[0-9a-f]{40}'` leaves only (a) current v26.10.1 subject/standing claims, (b) the explicitly dated History paragraph, (c) historical ALIVE-era evidence (2026-08-29 paragraphs, `receipts/release-v26.8.28-container.json`, issue #146), (d) the dated 2026-08-28 census note. Nothing stale remains unlabeled.
7. **Lane hygiene:** only the two files above written; vendor/* and all other lanes' files untouched (observed dirty from other lanes/coordinator; not modified by L5 — all vendor access was read-only `rev-parse/show/log/describe`).

## Commands + exits (all run 2026-10-01 in /Users/sac/ggen-ecosystem unless noted)

| cmd | exit | result |
|---|---|---|
| `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 | `release/v26.10.1` / `19a2b1f1` |
| `mkdir -p /tmp/v26101-lane5b` | 0 | scratch ready |
| `git status --porcelain docs/CURRENT-RELEASE-STANDING.md` | 0 | ` M` (pre-existing WIP, preserved) |
| `git diff HEAD --stat -- docs/CURRENT-RELEASE-STANDING.md` | 0 | WIP = +12/−5 vs HEAD |
| `git show HEAD:docs/CURRENT-RELEASE-STANDING.md \| sed -n '1,20p'` | 0 | HEAD pre-WIP text (old subject, `ALIVE`) |
| `git rev-parse origin/main` | 0 | `dc665a1e93573949040900faa65b46af3a3ea6d9` ✓ seam |
| `git -C vendor/ggen rev-parse v26.9.28^{commit}` | 0 | `ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e` ✓ seam |
| `git -C vendor/ggen rev-parse v26.10.0^{commit}` | 0 | `82795cda068d3d2a0571dd4228fd5d405982eff2` (tag exists) |
| `git -C vendor/ggen_igniter show 0abed8a35db68c18bba6982b266dd7546c162d1c:mix.exs \| grep -m1 '^version'` | 1 (no match) | contract's pattern missed indented line |
| `git -C vendor/ggen_igniter show 0abed8a35db68c18bba6982b266dd7546c162d1c:mix.exs \| grep -in version \| head -5` | 0 | line 9: `version: "26.9.30"` ✓ seam (matches lock) |
| `git -C vendor/ggen_igniter log -1 --format='%H %s' 0abed8a3...` | 0 | commit exists ("test: create ebin before compile_to_path...") |
| `git -C vendor/ggen-marketplace describe --tags bf9eccb3420134d4850dd49a5cbbef7dc35f20e2` | 0 | `v26.9.30-6-gbf9eccb34` ✓ seam |
| `git -C vendor/autofde-lab rev-parse origin/master` | 0 | `71de04a60db723764fab5afe042b42937b471e0e` ✓ seam |
| `git -C vendor/autofde-lab log -1 --format='%H %s' 71de04a6...` | 0 | "Merge pull request #210..." |
| `sed -n '/\[container\]/,/^\[/p' ecosystem.lock.toml` (worktree, post-L1) | 0 | tag `v26.10.1`, `standing = "BLOCKED"`, `requires_republish = true`, digest `sha256:6605878e...`, failure line, run `35833887166` @ `97620bdd` 2026-09-23T08:27:01Z |
| `git show HEAD:ecosystem.lock.toml \| sed -n '/\[container\]/,/^\[/p'` | 0 | pre-bump: tag `v26.9.29`, same digest, `requires_republish = true`, "v26.9.29 image not yet published" |
| `git log -S '6605878e' --format='%h %ad %s' --date=short -- ecosystem.lock.toml \| tail -3` | 0 | introduced by `327fd84c` 2026-09-23 "receipts(release): v26.9.22 container published and verified" |
| `git log --format='%h %ad %s' --date=short -8 -- ecosystem.lock.toml` | 0 | crown commits 2026-09-29/30, 2026-10-01 (grounds "v26.9.29 crown (2026-09-29)") |
| `git log --format='%h %ad %s' --date=short -5 -- docs/CURRENT-RELEASE-STANDING.md` | 0 | doc history (2026-08-29 corrections at HEAD) |
| `grep -nE 'v26\.[0-9]\|[0-9a-f]{40}' docs/CURRENT-RELEASE-STANDING.md` (pre- and post-write) | 0 | sweep; post-write = current claims + labeled history only |
| `git diff HEAD -- docs/CURRENT-RELEASE-STANDING.md` | 0 | full WIP diff reviewed before editing |

## REFUSED / BLOCKED / UNKNOWN items

- REFUSED_SEAM_CONFLICT: none. Every pinned seam value was independently reproduced (ancestor, ggen, marketplace, ggen_igniter sha+version, autofde-lab, container standing).
- BLOCKED: capsule standing written as `BLOCKED[AWAITING_PUBLISH]` (tag `v26.10.1`) — that is the deliverable content, stated as the lock records it; no publish/execution evidence exists or is claimed.
- UNKNOWN: none outstanding for this lane. Cited-not-re-witnessed item (explicitly labeled in the doc as decision-record-derived): the zero-asset property of ggen tag `v26.10.0`'s GitHub release object; tag existence verified locally, asset absence taken from RESOLUTIONS.md + lock `[ggen]`.
- Note for coordinator: the v26.9.25 and v26.9.29 crowns never published an image (both superseded awaiting republish); the last published image is the v26.9.22-era digest `sha256:6605878e...` (2026-09-23). The multi-arch gap (DoD item 8, PR-009) remains open history in the doc, unchanged.
