# L2 report — vendor-crown dossier

- lane: L2
- subject: `ggen-ecosystem` branch `release/v26.10.1` @ `19a2b1f1` (base `dc665a1e`)
- standing: COMPLETE (dossier written, UNSTAGED; no git state commands run by this lane)

## files-written

- `docs/releases/v26.10.1-vendor-crown.md` (new, UNSTAGED — no `git add`)
- `docs/jira/v26.10.1/lanes/L2-report.md` (this report)
- scratch (outside repo): `/tmp/v26101-lane2/` (`origin-head.txt`, `oldpins.txt`)

## decisions + rationale

1. Old-pin source reinterpreted by observation: RESOLUTIONS.md says pre-bump pins live in
   `HEAD`(=`dc665a1e`), but `git ls-tree` shows `HEAD` (`19a2b1f1`) AND `dc665a1e` both already
   carry gitlinks equal to the crown targets; the pre-bump pins exist only at
   `archive/pre-v26.10.1-dirty-20261001`. Distances were therefore computed
   `archive-pin → target`. This is NOT a seam conflict — every observed target string equals its
   pinned seam exactly; only the descriptive location of "old pins" differs. Flagged as
   OBSERVATION, not REFUSED_SEAM_CONFLICT. Consequence for the coordinator: the release branch
   already sits at target gitlinks, so `crown-submodules.py --apply` should be a no-op /
   verify-only pass on this subject.
2. autofde-lab default-branch anomaly recorded in the dossier (`master` vs the others' `main`),
   per contract; `origin/master` tip == target `71de04a6`.
3. Dossier states facts only; no standing claims (per contract item 3).

## commands + exits (all run from /Users/sac/ggen-ecosystem)

| command | exit |
|---|---|
| `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 (`release/v26.10.1`, `19a2b1f1`) |
| `git ls-tree HEAD vendor/<v>` ×6 | 0 (all == targets) |
| `git ls-tree archive/pre-v26.10.1-dirty-20261001 vendor/<v>` ×6 | 0 (pre-bump pins) |
| `git ls-tree dc665a1e93573949040900faa65b46af3a3ea6d9 vendor/<v>` ×6 | 0 (all == targets) |
| `git -C vendor/<v> rev-parse --abbrev-ref origin/HEAD` ×6 | 0 (autofde-lab=master, others=main) |
| `git -C vendor/autofde-lab log -1 --format='%H %ci %s' 71de04a6…` / `describe --tags` / `rev-list --count d5ac60ff..71de04a6` / `log --oneline … \| head -12` | 0 / 0 / 0 (819) / 0 |
| same quartet for beam4pm `57436870..7bad16ab` | 0 / 0 (`v26.9.9-777-g7bad16ab`) / 0 (483) / 0 |
| same quartet for ggen `06093e0c..ff96f04e` | 0 / 0 (`v26.9.28`) / 0 (208) / 0 |
| same quartet for ggen-marketplace `616e93d1..bf9eccb3` | 0 / 0 (`v26.9.30-6-gbf9eccb34`) / 0 (1455) / 0 |
| same quartet for ggen_igniter `d84da141..0abed8a3` | 0 / 0 (`v26.9.15-378-g0abed8a`) / 0 (376) / 0 |
| same quartet for wasm4pm `da48e98c..a7352d81` | 0 / 0 (`v26.9.30-5-ga7352d818`) / 0 (335) / 0 |
| `git -C vendor/<v> log -1 … <archive-pin>` + `describe --tags <archive-pin>` + `rev-parse origin/<default>` ×6 | 0 ×18 |
| (failed attempt, corrected) `set -- $pair` word-split loop → `git -C` fatal ×18 | 128 (zsh splitting; rerun with heredoc `while read` loop, all 0) |

Evidence from the failed zsh loop was discarded and fully re-collected; no value in the dossier
traces to a 128 exit.

## seam verification (L2 scope)

All six pinned target SHAs were recomputed independently and MATCH RESOLUTIONS.md:
`71de04a6…`, `7bad16ab…`, `ff96f04e…`, `bf9eccb3…`, `0abed8a3…`, `a7352d81…`.
Each target equals its vendor's origin default-branch tip (`rev-parse origin/<default>`).
No `REFUSED_SEAM_CONFLICT`.

## REFUSED / BLOCKED / UNKNOWN items

- REFUSED: none.
- BLOCKED: none.
- UNKNOWN: none.
- OBSERVATION (non-blocking): gitlinks at `HEAD`/`dc665a1e` already equal crown targets (see
  decision 1). Dossier records this as observed fact with source commands.
