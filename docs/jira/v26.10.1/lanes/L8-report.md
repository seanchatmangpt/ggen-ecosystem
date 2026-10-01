# L8 report — governor demand doc reconciliation (v26.10.1)

- lane: L8
- subject: `seanchatmangpt/ggen-ecosystem` branch `release/v26.10.1` @ `19a2b1f1` (verified first action)
- standing: **ALIVE** (verified NO-OP — every checkable claim in the doc grounded at HEAD; no release-keyed current claim exists to update)

## files-written

| file | action |
|---|---|
| `docs/MACRO-GOVERNOR-DEMAND.md` | **verified NO-OP — zero edits**. Preserved WIP correction (Environment hermeticity section, +10 lines vs HEAD) found intact in working tree; left UNSTAGED, untouched. |
| `docs/jira/v26.10.1/lanes/L8-report.md` | created (this report) |

## decision + rationale

**NO-OP, with the mandated sweep as evidence.**

1. Mandated sweep `grep -nE 'v26\.[0-9]|[0-9a-f]{40}|lock' docs/MACRO-GOVERNOR-DEMAND.md` returned exactly one hit:
   - line 3: `v26.9.26. Capability C17 / GGE-26922-14: ...` — a provenance stamp of the authoring
     commit `0a3a939d` (2026-09-25, "feat(governor): subject-keyed repair demand with close-on-recovery"),
     the same historical class as "introduced in 2ae7969a" (line 46). It states when the capability
     landed, not current standing. Zero 40-hex SHAs. Zero `lock` matches.
2. The doc contains none of the job's update targets: no demand rows justified by lock standing,
   no container BLOCKED rows, no governor run evidence tied to a lock sha, no open/closed issue
   counts (only historical examples "#365 and #366" — untouched per contract), no republish-pending
   state. Nothing keys this doc to `ecosystem.lock.toml` or the `[container]` seam, so RESOLUTIONS.md
   derived pins ([container] tag v26.10.1 / BLOCKED / requires_republish) have no anchor here.
3. Staleness check — every checkable factual claim grounded present at HEAD `19a2b1f1`:
   - tracked: `scripts/github_macro_governor.py`, `tests/test_github_macro_governor.py`,
     `docs/RECEIPT-SCHEMA.md`, `docs/STANDING.md`, `.github/workflows/github-macro-governor.yml`
     (`git ls-files --error-unmatch` exit 0).
   - all 5 named functions present (`fingerprint`, `dedupe_demands`, `existing_demand`,
     `reconcile_demands`, `hermetic_git_env` — grep count 5).
   - `GIT_LOCAL_ENV_VARS` present; all 7 standing tokens present (`DEMAND_ALREADY_EXISTS`,
     `RECOVERY_RECEIPT`, `NO_RECOVERY_RUN_ID`, `NO_RECOVERY_RECEIPT`, `ANCESTRY_UNKNOWN`,
     `DEMAND_RECOVERED`, `ACTION_BUDGET_EXHAUSTED`).
   The doc is capability semantics, release-independent; its content is as true at v26.10.1 as at
   v26.9.26. Rewriting the provenance stamp would falsify it (capability did not land in v26.10.1).

## commands + exits

| # | command | exit | result |
|---|---|---|---|
| 1 | `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 | `release/v26.10.1`, `19a2b1f1` |
| 2 | `grep -nE 'v26\.[0-9]|[0-9a-f]{40}|lock' docs/MACRO-GOVERNOR-DEMAND.md` | 0 | 1 match: line 3 `v26.9.26.` |
| 3 | `git status --porcelain docs/MACRO-GOVERNOR-DEMAND.md` | 0 | ` M` (WIP present on arrival) |
| 4 | `git diff HEAD --stat -- docs/MACRO-GOVERNOR-DEMAND.md` | 0 | 1 file changed, +10 insertions |
| 5 | `git diff HEAD -- docs/MACRO-GOVERNOR-DEMAND.md` | 0 | WIP = "Environment hermeticity" section (kept) |
| 6 | `git log --oneline -5 -- docs/MACRO-GOVERNOR-DEMAND.md` | 0 | single commit `0a3a939d` |
| 7 | `git show -s --format='%H %ci %s' 0a3a939d` | 0 | 2026-09-25 22:10:05 -0700, C17 / GGE-26922-14 |
| 8 | `git describe --contains 0a3a939d` | 128 | not contained in any tag in this clone (see UNKNOWN) |
| 9 | `git tag --contains 0a3a939d \| head -3` | 0 | empty |
| 10 | `git ls-files --error-unmatch` (5 referenced artifacts) | 0 | all tracked at HEAD |
| 11 | `grep -cE 'def (fingerprint\|dedupe_demands\|existing_demand\|reconcile_demands\|hermetic_git_env)\b' scripts/github_macro_governor.py` | 0 | 5 |
| 12 | token greps (`GIT_LOCAL_ENV_VARS`, 7 standing tokens) vs `scripts/github_macro_governor.py` | 0 | all present |
| 13 | `ls docs/jira/v26.10.1/lanes/` | 0 | empty before this report |

## REFUSED / BLOCKED / UNKNOWN items

- REFUSED_SEAM_CONFLICT: none — no pinned seam from RESOLUTIONS.md is contradicted (this doc keys to none of them).
- BLOCKED: none.
- UNKNOWN: `0a3a939d` is not reachable from any tag in this clone (`git describe --contains` exit 128,
  `git tag --contains` empty). The `v26.9.26.` stamp is read as the authored-era version label from the
  commit date + subject, not a tag-derived value; no pinned seam depends on it, so this does not alter
  the NO-OP decision.
- Note for coordinator: `docs/MACRO-GOVERNOR-DEMAND.md` enters integration still carrying the
  preserved WIP correction as unstaged `M` (+10 lines, hermeticity section) — unchanged by L8, by design.
