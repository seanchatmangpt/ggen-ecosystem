# v26.9.1 Jira Plan — ggen-ecosystem

Last Updated: 2026-09-01

## 1. Charter / Define

This repo (`ggen-ecosystem`) is mid-flight on a large automation-driven hardening
effort. Branch naming shows two concurrent programs:

- **`automation/ws1..ws5-*`** (~70 branches, 2026-08-28 to 2026-08-29): a scheduled,
  timestamped courts/fencing sweep. Each branch name follows
  `automation/wsN-YYYYMMDD-HHMM-<topic>-vN` and adds one narrowly-scoped
  test/contract ("fence X", "court Y", "activate Z consumer") — evidence of an
  automated DMEDI-style Measure/Explore loop running continuously against the repo's
  standing/ontology/receipt/Chicago-consumer surface.
- **`repair/*`, `feat/*`, `fix/*`, `docs/*`, `validate/*`, `handoff/*`** (2026-08-28 to
  2026-08-31): human/agent-driven consolidation branches taking the automation
  output and merging it toward a real mergeable state (publication-evidence
  contracts, GitHub DX/governance docs, container/CI qualification, supply-chain
  signing).

The most recent activity (last 24h, since 2026-08-31) narrows to exactly three
branches touched:

1. `origin/repair/chicago-evidence-boundary-20260829` — active repair branch,
   latest commit 2026-08-31 21:35 PDT, fixing workspace permissions after a
   root-owned Docker sync broke the Chicago-consumer test court.
2. `origin/main` — advanced via PR #200 (dependabot submodule bump), 2026-08-31
   15:20 PDT.
3. `origin/claude/ecosystem-docker-setup-4cfe41` — new branch, single commit,
   2026-08-31 10:56 PDT, adding a `SessionStart` hook to bring Docker up
   automatically on Claude Code web.

**v26.9.1 charter**: close the Chicago-evidence-boundary repair (the active,
in-flight branch as of this plan), land the Docker session-bootstrap convenience
branch, keep `main` moving via dependabot/submodule bumps, and use the ~70
automation branches as a queued backlog of "courts" to selectively promote rather
than merge wholesale. Scope explicitly excludes touching `main` directly in this
plan — this document only records the plan; execution follows in tracked PRs.

## 2. Measure — Current State (real `git log`/`git branch -a`, verified)

Verified via `git clone` of `https://github.com/seanchatmangpt/ggen-ecosystem.git`,
then `git branch -a` and `git log --all --since=2026-08-31` against the real
remote refs (no assumptions taken from branch names alone).

### 2.1 Branches touched since 2026-08-31 (real activity window)

| Branch | SHA | Date | Message |
|---|---|---|---|
| `repair/chicago-evidence-boundary-20260829` | `10f6564e` | 08-31 21:35 | fix(chicago): reclaim workspace permissions after docker sync |
| `main` | `25f363aa` | 08-31 15:20 | Merge PR #200 (dependabot submodules bump) |
| `claude/ecosystem-docker-setup-4cfe41` | `b7225335` | 08-31 10:56 | feat(session): add SessionStart hook for Docker |

No other of the ~100 remote branches has a commit dated on or after 2026-08-31;
the automation/ws*, feat/*, fix/*, docs/*, repair/*, validate/* branches (aside
from the three above) all stopped between 2026-08-28 and 2026-08-30.

### 2.2 `repair/chicago-evidence-boundary-20260829` detail

`git diff origin/main...origin/repair/chicago-evidence-boundary-20260829 --stat`:

```
.github/workflows/pr-governance.yml |  31 +-
Justfile                            |  12 +-
tests/chicago_consumer.sh           | 163 ++++++++++
tests/test_container_smoke.sh       | 587 +-----------------------------------
4 files changed, 204 insertions(+), 589 deletions(-)
```

7 commits ahead of `main`, ending in `10f6564e`. Commit sequence (oldest to
newest): `37c615c2` (route qualification to real consumer court) ->
`05453407` (add real fresh-consumer execution court) -> `9be4acd6`/`9be4abd6`
(remove synthetic standing from legacy smoke entrypoint) -> `367d8632` (require
real exact-head consumer execution) -> two merge-main commits (`7ae88b34`,
`bdcdeb7d`) reconciling with `main` as it advanced -> `10f6564e` (the permissions
fix, most recent). This branch is a genuine consolidation of the automation
courts' Chicago-consumer work into a real, currently-passing-shaped test surface,
replacing a 587-line legacy smoke test with a 163-line real consumer-execution
script.

### 2.3 `claude/ecosystem-docker-setup-4cfe41` detail

Single commit `b7225335`, 108 lines added across two files:
`.claude/hooks/session-start.sh` (94 lines, new) and `.claude/settings.json`
(14 lines, hook registration). Zero commits behind `main`'s tip at time of
branching (branches directly off a `main` at or near `25f363aa`). Self-contained,
additive, no deletions — low-risk to merge.

### 2.4 `main` recent history (context, not "since" window)

```
25f363aa Merge pull request #200 from seanchatmangpt/dependabot/submodules/submodules-81f41e3b29
25387e75 chore(submodules): bump vendor/autofde-lab in the submodules group
da16242a Merge PR #198: compose beam4pm into ecosystem container
e8708d79 compose beam4pm submodule into ecosystem container
cef697e0 Merge PR #195: sync-rail container safe.directory fix
```

`main` is actively receiving merged PRs from the repair/validate lineage
(PR #195, #198, #200), confirming the repair branches are the actual integration
path, not the raw automation/ws* branches.

### 2.5 Backlog: automation/ws1-ws5 courts (not touched since 2026-08-29, queued)

~70 branches across five worker streams (ws1-ws5), each a single narrowly-scoped
commit ("fence X", "test(...)", "feat(...)"). These are Measure/Explore-phase
artifacts (per this repo's own DMEDI-shaped automation) that have not yet been
selected for Develop/Implement. They represent the admissible search space this
plan's Explore phase draws candidates from, not branches this plan proposes to
merge directly.

## 3. Explore — Options Implied by Branch Names

Three non-dominated approaches to close v26.9.1, in order of increasing scope:

- **Option A — Minimal (repair-and-docker only)**: merge
  `claude/ecosystem-docker-setup-4cfe41` (additive, zero-risk) and finish/merge
  `repair/chicago-evidence-boundary-20260829` (already 7 commits of real
  consolidation). Leaves the ~70 automation/ws* branches as an explicit backlog
  for a future release. Lowest risk, fastest to a mergeable v26.9.1.
- **Option B — Selective court promotion**: Option A, plus hand-pick a small set
  of automation/ws* branches whose "court" content is still relevant against
  current `main` (e.g. `ws4-20260830-0238-publication-cells-054-103`, the most
  recent automation branch chronologically) and rebase/cherry-pick them forward.
  Requires per-branch conflict resolution (per the no-blanket-`-X theirs/ours`
  rule) since most automation branches are 2-4 days stale against `main`'s fast
  merge cadence.
- **Option C — Full ecosystem closure**: also reconcile the larger
  `feat/*`/`validate/*`/`replace/*` lineage (`feat/github-dx-qol-max-v3`,
  `validate/github-docker-integrated-v2`, `replace/scb-post-llm-agi`,
  `claude/ultracode-branch-merge-amiyd7`) which themselves already contain
  multi-branch merges of the automation backlog. Highest leverage (closes the
  most branches) but highest risk — several of these branches already show
  auto-resolved merge conflicts ("favoring incoming") in their own history,
  which is exactly the destructive-shortcut pattern this plan must avoid
  repeating when reconciling them against current `main`.

This plan recommends **Option A now**, with **Option B queued as the next
DMEDI cycle's Explore output** once Option A lands — matching the repo's own
worker-stream cadence rather than attempting Option C's full reconciliation in
one pass.

## 4. Develop — Concrete Next Engineering Steps

### 4.1 `claude/ecosystem-docker-setup-4cfe41`

1. Rebase onto current `main` tip (`25f363aa`) — branch is already based near
   there, so this should be a fast-forward or trivial rebase.
2. Verify `.claude/hooks/session-start.sh` is idempotent (safe to run on every
   session start, not just first) and does not assume a specific host Docker
   socket path — read the script and add a guard if missing.
3. Confirm `.claude/settings.json` hook registration does not collide with any
   existing `SessionStart` hook already on `main`.
4. No test suite changes needed (infra-only); manual verification: start a
   fresh session, confirm Docker comes up, confirm no error on a machine
   without Docker installed (should degrade, not fail the session).

### 4.2 `repair/chicago-evidence-boundary-20260829`

1. Re-run the two most recent merge-main reconciliation commits'-worth of diff
   against the *current* `main` tip (`25f363aa`) — the branch's own merge
   commits (`7ae88b34`, `bdcdeb7d`) were against an earlier `main`; confirm no
   new drift since PR #200 landed.
2. Run `tests/chicago_consumer.sh` (the new 163-line real consumer-execution
   court) against current `main` plus this branch's diff — this is the
   Chicago-style real-collaborator test this branch introduces; verify it
   passes for real, not from memory.
3. Confirm `tests/test_container_smoke.sh`'s 587-line reduction is a genuine
   dead-code removal (the legacy smoke entrypoint being retired) and not a
   silent coverage loss — diff the removed assertions against what
   `chicago_consumer.sh` now covers.
4. Confirm `.github/workflows/pr-governance.yml`'s 31-line change routes CI to
   the new consumer court correctly (the commit message says "route
   qualification to real consumer court").
5. Root-owned Docker file permission fix (`10f6564e`) — verify the actual file
   ownership issue is fixed by testing in a fresh container/CI runner, not
   just reading the patch.

### 4.3 Automation/ws* backlog (Option B, next cycle)

1. Rank the ~70 branches by (a) recency, (b) whether their target file/area
   still exists unmodified on current `main`, (c) whether the "court"/test they
   add is still relevant.
2. For each candidate, `git diff origin/main...origin/<branch>` individually
   (never batch-diff/batch-resolve) to assess real conflict surface before
   committing to a cherry-pick or rebase.
3. Defer this work to a follow-up plan (`docs/jira/v26.9.2/PLAN.md` or later)
   once Option A's two branches are merged and `main` has re-stabilized.

## 5. Implement — Merge Order, Gates, Rollout

### 5.1 Merge order

1. `claude/ecosystem-docker-setup-4cfe41` -> `main` first (lowest risk,
   additive-only, unblocks nothing but blocks on nothing either).
2. `repair/chicago-evidence-boundary-20260829` -> `main` second (higher-value,
   already the furthest-along consolidation branch; rebase onto `main` post-step
   1 before merging).
3. Automation/ws* selective promotion (Option B) deferred to next cycle —
   explicitly not part of this v26.9.1 merge order.

### 5.2 Verification gates (per branch, before merge)

- **Gate 1 — CI green on rebased HEAD**: both branches must pass
  `.github/workflows/pr-governance.yml` (and any other required checks) against
  a rebase onto `main`'s current tip, not the tip they were originally branched
  from.
- **Gate 2 — Real test run, not memory**: `tests/chicago_consumer.sh` executed
  locally or in CI with real output captured, per this repo's Chicago-style
  testing discipline (real collaborators, state-based assertions, no
  interaction-only mocks).
- **Gate 3 — No destructive conflict resolution**: any rebase conflict
  encountered while landing `repair/chicago-evidence-boundary-20260829` is
  resolved by reading both sides, never `-X theirs`/`-X ours` or a batch
  script.
- **Gate 4 — Docker hook degrade-safe**: `claude/ecosystem-docker-setup-4cfe41`
  confirmed not to hard-fail a session when Docker is unavailable.

### 5.3 Rollout and monitoring

- Land both branches via normal PR review (this plan does not open the PRs
  itself — separate action).
- After merge, monitor the next 3-5 `main` CI runs for regressions specifically
  in the Chicago-consumer court and container-smoke-test areas touched by
  `repair/chicago-evidence-boundary-20260829`'s 589-line test-file rewrite.
- Re-run this Measure phase (branch/commit inventory) at the start of the next
  cycle to pick up whichever automation/ws* branches are still relevant once
  `main` has absorbed these two merges — this is the standing re-verification
  step (a fresh `git log --all --since=<new-date>` sweep), not a one-time check
  assumed to hold.

## See Also

- `.github/workflows/pr-governance.yml` — CI gate referenced in Gate 1
- `tests/chicago_consumer.sh` — real consumer-execution court referenced in
  Gate 2 and Section 4.2
- `Justfile` — operator surface touched by the Chicago repair branch
