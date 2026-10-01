# v26.10.1 release bump — lane map (10 lanes, one canonical checkout)

Milestone: `v26.10.1` (vYY.M.D convention, date 2026-10-01).
Base: `origin/main` = `dc665a1e93573949040900faa65b46af3a3ea6d9` (local main ff'd from c9e305d7).
Branch: `release/v26.10.1` (all lanes write here; coordinator owns every git transition).
Pre-existing dirty state preserved at `archive/pre-v26.10.1-dirty-20261001`; doc corrections
re-applied onto the release branch (patch: `pre-existing-dirty-20261001.patch` in this dir).
Seam values pinned in `RESOLUTIONS.md` beside this file.

## Lanes (disjoint file ownership — two lanes never touch one file)

| lane | job | owned files (create/modify only these) |
|---|---|---|
| L1 | lock bump: all pins to v26.10.1-era values + `[ggen]` release decision w/ evidence + asset digests | `ecosystem.lock.toml` |
| L2 | vendor-crown dossier: per-vendor old→new SHA evidence | `docs/releases/v26.10.1-vendor-crown.md` (new) |
| L3 | changelog: `[v26.10.1]` entry; resolve 3-way conflict first | `CHANGELOG.md` |
| L4 | sync workflow + ontology pins (tag, marketplace_sha) | `.github/workflows/ggen-ecosystem-sync.yml`, `ontology.ttl` |
| L5 | current release standing doc → v26.10.1 subject | `docs/CURRENT-RELEASE-STANDING.md` |
| L6 | README pinned SHAs + standing line; resolve 3-way conflict first; CITATION.cff verify-only | `README.md`, `CITATION.cff` |
| L7 | ecosystem.ttl `dcterms:hasVersion` crown + TRANSPORT doc | `ecosystem.ttl`, `docs/TRANSPORT.md` |
| L8 | governor demand doc reconciliation | `docs/MACRO-GOVERNOR-DEMAND.md` |
| L9 | pre-bump court baseline receipts (court + crown dry-run) | `receipts/v26.10.1/*` (new dir only) |
| L10 | skeptic: independent seam recomputation vs RESOLUTIONS.md | `docs/releases/v26.10.1-seam-audit.md` (new) |

Shared-read files (read freely, write never): `ecosystem.lock.toml`, `RESOLUTIONS.md`, vendor/*.
Gitlink moves (`vendor/*`), `ggen.lock` regen, final court run, tag mint = **coordinator at integration**, not lanes.

## Law

- Agents never run git state commands (add/commit/checkout/branch/stash/push/submodule update). Read-only git (log/show/rev-parse/ls-remote/diff) allowed.
- Identical contract block in every dispatch prompt. Conflicts resolve on artifacts, not in chat.
- Standing vocabulary: `ALIVE | PARTIAL_ALIVE | BLOCKED | BUILD_BROKEN | UNKNOWN | UNSUPPORTED | REFUSED_*`. Every value written carries its source command in the lane report (`docs/jira/v26.10.1/lanes/L<N>-report.md`).
- Evidence contradicts a pinned seam → do not change the seam; flag `REFUSED_SEAM_CONFLICT` in the lane report.
- Integration (serialized, coordinator): apply lane commits atomically per lane → crown gitlinks via `scripts/crown-submodules.py --apply` to RESOLUTIONS.md targets → regen `ggen.lock` (`ggen sync`) → full court (`scripts/lock_crown_court.py`) → verify ladder → tag `v26.10.1` on release commit → draft PR.
