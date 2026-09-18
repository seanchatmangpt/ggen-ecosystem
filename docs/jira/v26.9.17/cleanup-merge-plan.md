# Cleanup and Merge Plan: ggen-ecosystem + ggen-marketplace (worktree/scratch family)

## Current State (as observed 2026-09-17)

Scope actually investigated: `/Users/sac/ggen-ecosystem` (its registered git worktrees)
plus `/Users/sac/ggen-marketplace-worktrees` (which turned out to be worktrees of a
*different* canonical repo, `/Users/sac/ggen-marketplace`, not of ggen-ecosystem).
Two adjacent plain-directory copies under that same marketplace family were found and
are noted for completeness but not deep-investigated (out of the requested scope).

### Family 1 — ggen-ecosystem

| Path | Type | Git status | Last commit | Size |
|---|---|---|---|---|
| `/Users/sac/ggen-ecosystem` | canonical repo | dirty: 2 untracked paths (`artifacts/`, `docs/jira/v26.9.15/`); on branch `fix/ggen-toml-stale-marketplace-sha-comment`; local `main` is 9 commits behind `origin/main` | `7e62e475` 2026-09-04 "fix(ggen.toml): correct stale ggen-marketplace SHA in [packs] comment" | 9.5G |
| `/private/tmp/wt-pr174` (worktree, branch `pr174-local`) | registered worktree | **directory already gone from disk** (`/private/tmp` was cleared) — `git worktree list` still shows it, `prunable` | n/a (dir gone) | 0B |
| `/private/tmp/claude-501/.../scratchpad/ggen-ecosystem-container-fix` (worktree, branch `fix/container-lock-stale-blocked-standing`) | registered worktree | directory already gone from disk, `prunable` | n/a | 0B |
| `/private/tmp/claude-501/.../scratchpad/wt-changelog` (worktree, branch `changelog-session-updates`) | registered worktree | directory already gone from disk, `prunable` | n/a | 0B |
| `/private/tmp/wt-main-check` (worktree, detached) | registered worktree | directory exists but is **empty** (0 files, no `.git`), `prunable` | n/a | 0B |
| `/private/tmp/wt-mfact` (worktree, branch `repair/mfact-marketplace-drift-20260902211340`) | registered worktree | directory already gone from disk, `prunable` | n/a | 0B |
| `/private/tmp/wt-pr159` (worktree, branch `feat/github-max-dx-qol-20260829-r2`) | registered worktree | directory already gone from disk, `prunable` | n/a | 0B |
| `/private/tmp/wt-pr164` (worktree, branch `dependabot/github_actions/github-actions-c1aec2c850`) | registered worktree | directory already gone from disk, `prunable` | n/a | 0B |
| `/private/tmp/wt-pr201` (worktree, branch `feat/g07-release-gate-rebuild-v2`) | registered worktree | directory exists but contains only a stray empty `vendor/` subdir, no `.git`, `prunable` | n/a | 0B |
| `/private/tmp/wt-pr225` (worktree, branch `feat/local-github-dfcm-runtime`) | registered worktree | directory exists but contains only a stray empty `vendor/` subdir, no `.git`, `prunable` | n/a | 0B |

`git worktree list` in `/Users/sac/ggen-ecosystem` registers all 9 of the above as
worktrees; `git worktree prune -v --dry-run` confirms every one of them would be
removed ("gitdir file points to non-existent location") because the backing
directories under `/private/tmp/**` and the container-fix/wt-changelog scratchpad
paths no longer exist (or are empty) — `/private/tmp` is ephemeral on this machine and
was evidently cleared since those worktrees were created. **The branches themselves
still exist and are intact** in `/Users/sac/ggen-ecosystem/.git` — only the worktree
checkouts (the extra working directories) are gone. Local branch tracking state
(`git branch -vv`, full list):

| Local branch | Tip | Upstream tracking |
|---|---|---|
| `changelog-session-updates` | `eff1cf1d` | `origin/changelog-session-updates` (in sync) |
| `chore/autofde-lab-pin-sync` | `bd884019` | `origin/main`: ahead 3, behind 16 |
| `dependabot/github_actions/github-actions-c1aec2c850` | `f9e5fde2` | `origin/dependabot/...` (in sync) |
| `feat/g07-release-gate-rebuild-v2` | `2867e9c8` | `origin/feat/g07-release-gate-rebuild-v2` (in sync) |
| `feat/github-max-dx-qol-20260829-r2` | `79537eb4` | `origin/feat/github-max-dx-qol-20260829-r2` (in sync) |
| `feat/local-github-dfcm-runtime` | `c60a6577` | `origin/feat/local-github-dfcm-runtime` (in sync) |
| `fix/container-lock-stale-blocked-standing` | `fcdea61f` | `origin/fix/container-lock-stale-blocked-standing` (in sync) |
| `fix/ggen-toml-stale-marketplace-sha-comment` (**current HEAD**) | `7e62e475` | `origin/fix/ggen-toml-stale-marketplace-sha-comment` (in sync) |
| `fix/mfact-certification-historical-drift` | `7440bb4d` | `origin/main`: ahead 1, behind 13 |
| `fix/pragprog-tps-hardcoded-marketplace-sha` | `c33d7fb2` | `origin/main`: ahead 1, behind 11 |
| `main` | `bc026f5a` | `origin/main`: behind 9 |
| `pr159-rebase` | `d89242de` | none (no upstream) |
| `pr164-work` | `d89242de` | none (no upstream) |
| `pr174-local` | `6ba44359` | none (no upstream) |
| `pr201-worklocal` | `f86b69c1` | `origin/main`: behind 18 |
| `pr225-work` | `f86b69c1` | `origin/main`: behind 18 |
| `repair/chicago-evidence-boundary-20260829` | `d89242de` | none (no upstream) |
| `repair/mfact-marketplace-drift-20260902211340` | `780781e8` | `origin/repair/mfact-marketplace-drift-20260902211340` (in sync) |

Remote: `origin = https://github.com/seanchatmangpt/ggen-ecosystem` (fetch+push).

### Family 2 — ggen-marketplace (the actual owner of `~/ggen-marketplace-worktrees`)

| Path | Type | Git status | Last commit | Size |
|---|---|---|---|---|
| `/Users/sac/ggen-marketplace` | canonical repo | 2 untracked paths (`docs/jira/v26.9.15/`, `packages/marketplace-cli/.ggen_igniter/`); on branch `main`; local `main` is **2 commits ahead of `origin/main`** (unpushed: `14a13986` "fix(marketplace-cli): oracle tests..." and `e7954ff6` "docs(ex-noun-verb-cli-pack): greet-cli README...") | `14a13986` 2026-09-15 | 5.5G |
| `/Users/sac/ggen-marketplace-worktrees/feat-ash-extension-pack-doc-template` | real git worktree of `ggen-marketplace` (confirmed via `git worktree list` in the canonical repo) | clean (`git status --short` empty) | `314d1102` 2026-09-16 "feat(ash-extension-pack): scripts-index doc family..." — branch is **2 commits ahead of `main`**, pushed to `origin/feat/ash-extension-pack-doc-template`, not yet merged | 2.7G |
| `/Users/sac/ggen-marketplace-worktrees/feat-ash-extension-pack-license-file` | real git worktree of `ggen-marketplace` | clean (`git status --short` empty) | `832e2c1c` 2026-09-16 "feat(ash-extension-pack): license-file family..." — branch is **1 commit ahead of `main`**, pushed to `origin/feat/ash-extension-pack-license-file`, not yet merged | 2.7G |
| `/Users/sac/ggen-marketplace-bridged-packs` | plain directory, **not a git repo** (`git rev-parse` fails: no `.git`) | n/a | n/a | 660K |
| `/Users/sac/ggen-marketplace-wip-staging` | plain directory, **not a git repo** (contains one loose subfolder `xaas-ash-core-pack/`, no `.git`) | n/a | n/a | 60K |

Remote: `origin = https://github.com/seanchatmangpt/ggen-marketplace` (fetch+push).

### Out-of-scope note (not investigated this pass)

A home-directory scan turned up a much larger population of `*-worktrees`, `*-wt`,
`.scratch-*`, `*-backup*`, `*.bak`, and `*_copy` directories unrelated to
ggen-ecosystem/ggen-marketplace (e.g. `ex4pm-worktrees`, `wasm4pm-worktrees`,
`ash_a2a-wt`, `ash-surface-wt`, `zoela-wt`, `wasm4pm_copy`, `clnrm-backup-*`,
`gitvan-backup-*`, several multi-hundred-MB `.tar.gz` backups). These are real and
listed under Open Questions below, but were not individually git-inspected — that is
a separate cleanup pass, scoped explicitly if wanted.

## What "merged" should look like

### ggen-ecosystem family

**Canonical going forward: `/Users/sac/ggen-ecosystem`.** It is the only path in this
family with an actual working directory left on disk — every other registered
worktree's backing directory is already gone or empty (evidence: `git worktree prune
--dry-run` flags all 9 as prunable; direct `ls`/`git -C` checks against
`/private/tmp/wt-pr201` and `/private/tmp/wt-pr225` show only a stray empty `vendor/`
dir, and `/private/tmp/wt-main-check` and the four scratchpad-rooted paths are gone
entirely). No data lives only in those worktree checkouts — the branches they pointed
to are intact in the canonical repo's own `.git`, and 6 of the 9 branches are also
already pushed to `origin`.

For every other path in this family:

- **The 9 stale worktree registrations** (`pr174`, `container-fix`, `wt-changelog`,
  `wt-main-check`, `wt-mfact`, `wt-pr159`, `wt-pr164`, `wt-pr201`, `wt-pr225`): no
  merge needed. The backing directories are already gone/empty, so there is nothing to
  cherry-pick. This is pure metadata cleanup — `git worktree prune` is safe to run
  directly with no prior review step, because pruning cannot lose data (the data is
  already gone from disk; the branches themselves survive independently in
  `.git/refs/heads` and are not touched by `worktree prune`).
- **Branches with no upstream** (`pr159-rebase`, `pr164-work`, `pr174-local`,
  `repair/chicago-evidence-boundary-20260829`) all point at the same tip `d89242de`
  ("fix(ci): serialize act-container's build-amd64/build-arm64 jobs") or `6ba44359`
  for `pr174-local` — this is local-only work not on `origin`. **MANUAL REVIEW
  REQUIRED**: confirm whether this commit already landed on `main` under a different
  branch/PR (it looks like a PR-staging rename artifact — four branch names for what
  may be the same fix) before deleting these branches, since deleting an unpushed
  branch is the one truly irreversible step in this family.
- **`pr201-worklocal` / `pr225-work`**: both track `origin/main` directly (behind 18)
  at tip `f86b69c1`, same commit as the already-gone `wt-pr201`/`wt-pr225` worktrees.
  Since their upstream is literally `origin/main`, they carry no unique work beyond
  what a PR already captured (`feat/g07-release-gate-rebuild-v2` /
  `feat/local-github-dfcm-runtime`, both already pushed and tracked cleanly). Safe to
  delete as local branches once confirmed merged/superseded (see commands below), no
  cherry-pick needed.
- **The 6 in-sync feature/repair branches** (`changelog-session-updates`,
  `dependabot/...`, `feat/g07-release-gate-rebuild-v2`, `feat/github-max-dx-qol-...`,
  `feat/local-github-dfcm-runtime`, `fix/container-lock-stale-blocked-standing`,
  `repair/mfact-marketplace-drift-...`) are already fully pushed to `origin` under
  their own names — they are not blocked on anything local; whether they are safe to
  delete locally depends only on whether their PRs have merged on GitHub, which was
  not checked here (no `gh` calls were made — read-only git/du only, per the
  investigation constraint). **MANUAL REVIEW REQUIRED**: check PR merge state on
  GitHub before deleting any of these local branches.
- **`/Users/sac/ggen-ecosystem` itself** (canonical): has 2 untracked paths
  (`artifacts/`, `docs/jira/v26.9.15/`) and is 9 commits behind `origin/main` while
  sitting on a feature branch. Untracked, uncommitted work — **MANUAL REVIEW
  REQUIRED**: decide whether `artifacts/autonomic-crown.json` and
  `docs/jira/v26.9.15/` are intentional WIP to commit or stray output to delete
  before this repo is treated as the clean canonical base.

### ggen-marketplace family (the actual home of `~/ggen-marketplace-worktrees`)

**Canonical going forward: `/Users/sac/ggen-marketplace`.** It is the repo the two
`ggen-marketplace-worktrees/*` directories are real git worktrees *of* (confirmed by
running `git worktree list` inside it — both paths and branches match exactly), it
carries the `origin` remote, and it has the longest, most current history (`main` at
`14a13986`, 2026-09-15, only 2 commits ahead of `origin/main`).

- **`ggen-marketplace-worktrees/feat-ash-extension-pack-doc-template`**: clean
  worktree (no uncommitted changes), branch is 2 commits ahead of `main` and already
  pushed to `origin/feat/ash-extension-pack-doc-template`. Safe to `git worktree
  remove` directly (no data loss — everything is on `origin`), but do **not** delete
  the branch itself until its PR is merged into `main` — it is not yet merged (2
  commits present on the branch, 0 present on `main`, confirmed via `git rev-list
  --left-right --count main...feat/ash-extension-pack-doc-template` → `0  2`).
- **`ggen-marketplace-worktrees/feat-ash-extension-pack-license-file`**: same
  situation — clean, 1 commit ahead of `main`, pushed to
  `origin/feat/ash-extension-pack-license-file`, not yet merged
  (`main...feat/ash-extension-pack-license-file` → `0  1`). Safe to `git worktree
  remove` directly; keep the branch until merged.
- **`/Users/sac/ggen-marketplace` itself** (canonical): 2 local commits ahead of
  `origin/main` that are not yet pushed. **MANUAL REVIEW REQUIRED**: push these (or
  confirm they are superseded elsewhere) before treating `main` as fully
  reconciled with `origin`. Also has 2 untracked paths
  (`docs/jira/v26.9.15/`, `packages/marketplace-cli/.ggen_igniter/`) to review.
- **`/Users/sac/ggen-marketplace-bridged-packs`** and
  **`/Users/sac/ggen-marketplace-wip-staging`**: plain directories, not git repos at
  all (no `.git`). They cannot be merged via git. **MANUAL REVIEW REQUIRED**: someone
  has to look at their contents by hand and decide whether anything in them (e.g.
  `wip-staging/xaas-ash-core-pack/`) is unique work that should be copied into a real
  branch of `ggen-marketplace` before these folders are deleted — git tooling cannot
  make this determination.

## Commands to run (in order), once approved

```bash
# --- ggen-ecosystem family ---

# 1. Purely metadata cleanup: remove the 9 stale worktree registrations.
#    Safe unconditionally -- the backing directories are already gone or empty,
#    and this command does not touch any branch or ref.
cd /Users/sac/ggen-ecosystem
git worktree prune -v

# 2. MANUAL REVIEW REQUIRED (do not run yet): confirm on GitHub which of these
#    branches' PRs have merged before deleting the local branch pointers.
#    Once confirmed merged, delete with (repeat per branch):
#      git branch -d changelog-session-updates
#      git branch -d dependabot/github_actions/github-actions-c1aec2c850
#      git branch -d feat/g07-release-gate-rebuild-v2
#      git branch -d feat/github-max-dx-qol-20260829-r2
#      git branch -d feat/local-github-dfcm-runtime
#      git branch -d fix/container-lock-stale-blocked-standing
#      git branch -d repair/mfact-marketplace-drift-20260902211340
#    (-d refuses if not fully merged into HEAD's history -- that refusal is the
#    safety check; do not force with -D without re-verifying on GitHub first.)

# 3. MANUAL REVIEW REQUIRED (do not run yet): pr159-rebase, pr164-work,
#    pr174-local, repair/chicago-evidence-boundary-20260829 have no upstream --
#    confirm their commit (d89242de / 6ba44359) already landed under a tracked
#    branch name before deleting:
#      git log -1 --format=%H d89242de
#      git branch --contains d89242de
#    Only after confirming it's duplicated elsewhere:
#      git branch -D pr159-rebase pr164-work pr174-local repair/chicago-evidence-boundary-20260829

# 4. MANUAL REVIEW REQUIRED (do not run yet): pr201-worklocal / pr225-work track
#    origin/main directly and are 18 commits behind -- confirm their unique tip
#    f86b69c1 is superseded by the pushed feat/g07-release-gate-rebuild-v2 /
#    feat/local-github-dfcm-runtime branches, then:
#      git branch -d pr201-worklocal pr225-work

# 5. MANUAL REVIEW REQUIRED (do not run yet): the canonical repo itself has
#    uncommitted untracked paths -- inspect, then either commit or remove:
#      git status --short
#      # review artifacts/autonomic-crown.json and docs/jira/v26.9.15/ by hand
#      # then EITHER:
#      git add artifacts/ docs/jira/v26.9.15/ && git commit -F <message-file>
#      # OR, if confirmed disposable:
#      rm -rf artifacts/ docs/jira/v26.9.15/

# --- ggen-marketplace family ---

# 6. Safe once confirmed the branches are pushed (already verified above --
#    origin/feat/ash-extension-pack-doc-template and
#    origin/feat/ash-extension-pack-license-file both exist and match):
cd /Users/sac/ggen-marketplace
git worktree remove /Users/sac/ggen-marketplace-worktrees/feat-ash-extension-pack-doc-template
git worktree remove /Users/sac/ggen-marketplace-worktrees/feat-ash-extension-pack-license-file
# then, only after each branch's PR is confirmed merged on GitHub:
#   git branch -d feat/ash-extension-pack-doc-template
#   git branch -d feat/ash-extension-pack-license-file

# 7. MANUAL REVIEW REQUIRED (do not run yet): push or reconcile the 2 local-only
#    commits on ggen-marketplace's main before treating it as caught up with origin:
#      git -C /Users/sac/ggen-marketplace log origin/main..main --oneline
#      # review, then:
#      git -C /Users/sac/ggen-marketplace push origin main

# 8. MANUAL REVIEW REQUIRED (do not run yet, and not automatable): inspect
#    ggen-marketplace-bridged-packs/ and ggen-marketplace-wip-staging/ by hand for
#    unique content, since neither is a git repo and git cannot diff them against
#    anything:
#      ls -la /Users/sac/ggen-marketplace-bridged-packs
#      ls -la /Users/sac/ggen-marketplace-wip-staging/xaas-ash-core-pack
#      # if nothing unique found:
#      # rm -rf /Users/sac/ggen-marketplace-bridged-packs /Users/sac/ggen-marketplace-wip-staging
```

## Open questions

- **PR merge state on GitHub was not checked** (this investigation was restricted to
  local git/du/ls; no `gh` or network calls were made). Every "delete this branch"
  step above needs a real look at `github.com/seanchatmangpt/ggen-ecosystem/pulls` and
  `github.com/seanchatmangpt/ggen-marketplace/pulls` before it can be run non-manually.
- **Why do 4 ggen-ecosystem branches (`pr159-rebase`, `pr164-work`, `pr174-local`,
  `repair/chicago-evidence-boundary-20260829`) share tip `d89242de`/`6ba44359` with no
  upstream?** This looks like leftover PR-staging renames from an earlier session, but
  git alone can't say whether they're intentional duplicates kept as a paper trail or
  accidental strays — needs the user's own memory of that session.
- **`/Users/sac/ggen-ecosystem`'s untracked `artifacts/` and `docs/jira/v26.9.15/`,
  and `ggen-marketplace`'s untracked `docs/jira/v26.9.15/` and
  `packages/marketplace-cli/.ggen_igniter/`** — cannot tell from git alone whether
  these are intentional in-progress work or accidental stray output; needs the user to
  look.
- **`ggen-marketplace-bridged-packs/` (660K) and `ggen-marketplace-wip-staging/`
  (60K)** are plain, non-git directories with no way to diff them against the
  canonical repo's history — a human has to eyeball their contents.
- **The user's original request said "the `~/` worktrees temps scratch etc"**, which
  is broader than the two paths this plan actually investigated. A home-directory
  listing surfaced many more candidates outside this repo family — `ex4pm-worktrees`,
  `wasm4pm-worktrees`, `wasm4pm_copy`, `wasm4pm-compat_copy`, `ash_a2a-wt`,
  `ash-surface-wt`, `zoela-wt`, `praxis-hierarchical-projection-wt`,
  `unibit-overnight-worktree`, `xaas-worktrees`, several `.scratch-*` dirs, several
  `*-backup-*` directories/tarballs (some hundreds of MB each), and a bare
  `/Users/sac/worktrees` directory. None of these were git-inspected in this pass
  (out of the requested "ggen-ecosystem + ggen-marketplace-worktrees" scope) — if the
  intent was the whole home directory, that needs its own pass with the same
  discover→verify structure used here, repo family by repo family.
- **"deleted gemma manually"** (from the original request) — no `gemma`-named
  directory was found under `/Users/sac` during this investigation, consistent with
  it already being removed; no further action taken on it here.

## Merge Execution Log (2026-09-17)

Content-level evaluation/merge pass per user instruction: **no deletion of any file,
directory, worktree, or branch** — that is handled separately. Every action below is
additive (new commit and/or new pushed branch on the existing `origin` remote); no
`git worktree remove`, `git branch -d/-D`, `rm`, `git clean`, `git checkout -- <path>`,
or `git reset --hard` was run at any point in this pass.

### Re-verified current state first

- Re-ran `git fetch origin --prune` in both `ggen-ecosystem` and `ggen-marketplace`.
  `ggen-ecosystem`'s `origin/main` had moved forward significantly since the plan doc
  was written (`e74bc5d..15305ce`, plus many new remote branches/tags) — local `main`
  was still untouched (no local-only commits on `main`, confirmed via `git branch -vv`
  showing `[origin/main: behind 9]` with no "ahead"), so nothing needed pushing there.
- Re-confirmed all 9 stale worktree registrations, the branch-tracking table, and the
  two `ggen-marketplace` worktrees' clean/ahead status from the original plan doc
  still hold as described — no drift beyond `origin/main` advancing.

### Actions taken (real commits/pushes)

1. **`ggen-marketplace` — pushed the 2 pre-existing local-only commits on `main`**
   (this resolves the plan's item 7 / "MANUAL REVIEW REQUIRED: push these... before
   treating main as fully reconciled"). Fast-forward push, same branch/remote already
   configured:
   ```
   git -C /Users/sac/ggen-marketplace push origin main
   # a24193705..14a13986 main -> main
   ```
   `main` is now `14a13986` == `origin/main`, confirmed via `git log origin/main..main`
   returning empty.

2. **`ggen-marketplace` — captured the untracked `docs/jira/v26.9.15/` review record**
   (a real, completed 14-hour cross-repo review, ticket GMKT-2601, never previously
   committed). Committed and pushed directly to `main` (purely additive new files,
   no conflict with the concurrent push in step 1):
   ```
   commit 800b8c6c5d05e91ff3b2d3bbd99c095acbe09359
   "docs(jira): capture v26.9.15 cross-repo review record (consolidation court negative result)"
   git -C /Users/sac/ggen-marketplace push origin main
   # 14a13986..800b8c6c main -> main
   ```
   `packages/marketplace-cli/.ggen_igniter/` (the other untracked path) was
   deliberately **left alone, uncommitted** — inspection showed it is a local
   `ggen_igniter` tool-run cache (a `manifest.json` + receipts `.jsonl` referencing
   `tmp_verify/` scratch paths under `packages/marketplace-cli/`), not source content.
   Committing a tool cache into history is not a clearly-safe additive action, so it
   was left exactly as found rather than guessed at either way — see Still Open.

3. **`ggen-ecosystem` — captured the untracked `artifacts/` and
   `docs/jira/v26.9.15/`** (resolves the plan's "MANUAL REVIEW REQUIRED: decide
   whether `artifacts/autonomic-crown.json` and `docs/jira/v26.9.15/` are intentional
   WIP to commit or stray output"). Inspection confirmed both are real, completed
   work-product (a submodule-pin receipt matching the `autonomic-crown/v2` schema,
   and another completed cross-repo review record, ticket GECO-2601) — genuinely
   valuable, not accidental output, and neither path exists anywhere else in this
   repo's git history (`git log --all -- <path>` returned empty for both before this
   commit). Rather than committing directly onto the checked-out feature branch
   (`fix/ggen-toml-stale-marketplace-sha-comment`, already merged as PR #267) or onto
   a stale local `main` that is far behind `origin/main`, this was captured on a new,
   dedicated, purely-additive branch and pushed:
   ```
   git checkout -b docs/capture-v26.9.15-review-and-crown-receipt
   commit 73488412f6ad45ccff9e9d0f621996ab50789beb
   "docs(jira): capture v26.9.15 cross-repo review record + autonomic-crown receipt"
   git push -u origin docs/capture-v26.9.15-review-and-crown-receipt
   # new branch -> origin/docs/capture-v26.9.15-review-and-crown-receipt
   ```
   Then switched back to `fix/ggen-toml-stale-marketplace-sha-comment` (the branch
   this session found checked out), leaving the working tree exactly as originally
   found aside from the now-committed-and-pushed content (verified: `git status
   --short` shows only the untracked `docs/jira/v26.9.17/` — this plan doc's own
   directory — remaining, unchanged from before this session started).
   This new branch is **not yet merged into `main`** — that PR-open/merge decision is
   left for the user (see Still Open).

### Investigated and resolved as "no action needed" (content already safe)

- **The four no-upstream branches (`pr159-rebase`, `pr164-work`, `pr174-local`,
  `repair/chicago-evidence-boundary-20260829`) sharing tip `d89242de`/`6ba44359`** —
  the plan's open question ("why do 4 branches share this tip with no upstream?") is
  now answered: `git branch -r --contains 6ba44359` shows `6ba44359` (and by the same
  commit message, `d89242de`) is an **old, superseded snapshot** of what is now
  `origin/repair/chicago-evidence-boundary-20260829` at a completely different SHA
  (confirmed via `git merge-base --is-ancestor` → not an ancestor; a 407-file diff
  between the two tips; `gh pr list` shows this is PR #174, still OPEN). The local
  branches are stale pre-rewrite copies, not unique unpushed work — their content is
  already present, in more current form, on `origin` under the PR #174 branch. No
  cherry-pick was needed or performed. (Branches themselves left untouched per the
  no-deletion constraint.)
- **`pr201-worklocal` / `pr225-work`** (tip `f86b69c1`) — confirmed via
  `git branch -r --contains f86b69c1` that this tip is an ancestor of `origin/main`
  and of the already-pushed `feat/g07-release-gate-rebuild-v2` /
  `feat/local-github-dfcm-runtime` branches (PR #199, already merged). No unique
  content; nothing to push.
- **The 6 "in-sync" feature/repair branches** — checked real PR merge state via
  `gh pr list --repo seanchatmangpt/ggen-ecosystem --state all`:
  - `changelog-session-updates` -> PR #273 **MERGED** 2026-09-05
  - `fix/container-lock-stale-blocked-standing` -> PR #268 **MERGED** 2026-09-05
  - `dependabot/github_actions/github-actions-c1aec2c850` -> PR #164 **CLOSED**
    (not merged; superseded by newer dependabot PRs, e.g. currently-open #329 — a
    version-bump branch, not unique content)
  - `feat/g07-release-gate-rebuild-v2` -> PR #201 **OPEN**, already pushed to
    `origin` under its own name; content is safe regardless of local branch fate
  - `feat/github-max-dx-qol-20260829-r2` -> PR #159 **OPEN**, already pushed
  - `repair/mfact-marketplace-drift-20260902211340` -> PR #229 **OPEN**, already
    pushed
  - `feat/local-github-dfcm-runtime` -> PR #225 **OPEN**, already pushed
  - `chore/autofde-lab-pin-sync` -> PR #248 **MERGED**; `fix/mfact-certification-
    historical-drift` -> PR #263 **MERGED**; `fix/pragprog-tps-hardcoded-
    marketplace-sha` -> PR #266 **MERGED**; `fix/ggen-toml-stale-marketplace-sha-
    comment` (the branch checked out at session start) -> PR #267 **MERGED**.
  Every branch's content is confirmed present on `origin` (either merged into `main`
  or as its own pushed branch backing an open PR) — no cherry-picking needed. Whether
  to delete the now-superfluous local branch pointers is exactly the
  merge-into-main-or-not judgment call this task was told not to make; left for the
  separate deletion pass (see Still Open).

### `ggen-marketplace` worktree branches (`feat/ash-extension-pack-doc-template`,
`feat/ash-extension-pack-license-file`)

Both worktrees re-verified clean (`git status --short` empty in each). Checked
`gh pr list --head <branch>` for both — **neither has an open or merged PR** on
`ggen-marketplace` (empty result for both). Content is safe on `origin` (confirmed
`origin/feat/ash-extension-pack-doc-template` and
`origin/feat/ash-extension-pack-license-file` exist and match the worktree tips), but
opening a PR / deciding whether and how to land these into `main` is a code-review
judgment call outside this pass's additive-merge scope — left for the user.

### Non-git plain directories re-inspected

- **`/Users/sac/ggen-marketplace-bridged-packs`** (150+ `*.toml` files, 660K) —
  opened several sample files; each one carries a `[pack.metadata] bridged_from =
  "~/ggen-marketplace/packs/<name>"` field pointing back at a pack that already
  exists in the canonical `ggen-marketplace/packs/` tree (verified for
  `tcps-core-pack` as a sample: `packs/tcps-core-pack` exists in canonical). This
  directory is a **generated bridge/pointer index into the canonical repo**, not
  independent source content — there is nothing here to merge. No subtree import
  performed (the hard-constraint subtree guidance applies to independent repos with
  real unique content in both; this directory is neither independent nor unique).
- **`/Users/sac/ggen-marketplace-wip-staging/xaas-ash-core-pack`** (60K) — inspected
  fully. The canonical `ggen-marketplace/packs/xaas-ash-core-pack/` already exists
  and is far more complete (has `templates/`, `queries/`, `tests/`, `README.md`,
  `DIFFICULTIES.md`, etc.). The staging copy's only content beyond tool-run state is
  `templates-hooks/README.md`, a design-rationale note about why frontmatra-requiring
  templates are kept in a separate directory from `templates/`. **This directory also
  contains real private key material**
  (`xaas-ash-core-pack/.ggen/keys/signing.key`, `verifying.key`) alongside a
  `.ggen-v2/receipt.json` tool-run receipt. Per the hard constraint ("if you are not
  fully confident an action is safe and purely additive, do NOT do it"), **nothing
  was copied from this directory** — copying its contents wholesale risked committing
  key material into git history, and the one plausibly-unique file
  (`templates-hooks/README.md`) was not confidently determined to be absent from the
  canonical pack's own `README.md`/`DIFFICULTIES.md`. Left exactly as found; flagged
  for human review (see Still Open).

### Still Open (for the user / the separate deletion pass)

- **Now safe to prune once confirmed** (metadata-only, no data loss — but left
  untouched here since worktree pruning is a form of the "worktree" deletion this
  task was told to leave to the separate pass): the 9 stale worktree registrations in
  `ggen-ecosystem` (`git worktree prune -v`).
- **Local branch pointers safe to delete once the user confirms**, since their
  content is verified present on `origin` per the merge-state findings above:
  `changelog-session-updates`, `fix/container-lock-stale-blocked-standing`,
  `chore/autofde-lab-pin-sync`, `fix/mfact-certification-historical-drift`,
  `fix/pragprog-tps-hardcoded-marketplace-sha` (all merged); `pr201-worklocal`,
  `pr225-work` (superseded by merged PR #199 content); `pr159-rebase`, `pr164-work`,
  `pr174-local`, `repair/chicago-evidence-boundary-20260829` (stale pre-rewrite
  snapshots, superseded by current `origin/repair/chicago-evidence-boundary-20260829`
  under still-open PR #174 — do not delete the *remote* branch, only these stale
  local copies would be candidates). `dependabot/github_actions/github-actions-
  c1aec2c850` is a closed/superseded dependabot branch, also a deletion candidate.
  `feat/g07-release-gate-rebuild-v2`, `feat/github-max-dx-qol-20260829-r2`,
  `feat/local-github-dfcm-runtime`, `repair/mfact-marketplace-drift-20260902211340`
  back still-**open** PRs (#201, #159, #225, #229) — do **not** delete these; they are
  live review branches.
- **`ggen-ecosystem` new branch `docs/capture-v26.9.15-review-and-crown-receipt`**
  (commit `73488412`, pushed to `origin`) needs a human decision: open a PR and merge
  into `main`, or handle differently. Content is safe on `origin` either way.
- **`ggen-marketplace-worktrees/feat-ash-extension-pack-doc-template` and
  `feat-ash-extension-pack-license-file`**: both clean, both pushed to `origin`, both
  with no PR open. Decide whether to open PRs and merge into `ggen-marketplace`'s
  `main`; once merged (or abandoned), the worktrees become safe deletion candidates
  for the separate pass.
- **`packages/marketplace-cli/.ggen_igniter/`** in `ggen-marketplace` — left
  uncommitted; likely belongs in `.gitignore` rather than either committed or
  deleted, but that is a repo-hygiene decision for the user.
- **`ggen-marketplace-wip-staging/xaas-ash-core-pack`** — contains real private key
  material (`signing.key`, `verifying.key`); a human must decide whether to rotate/
  discard those keys and whether `templates-hooks/README.md`'s design rationale is
  genuinely absent from the canonical pack (if so, worth hand-copying just that one
  file — not automated here). Once resolved, this directory (and
  `ggen-marketplace-bridged-packs`, confirmed a pure generated pointer index with
  nothing unique) become candidates for the separate deletion pass.
- All previously-listed Open Questions in this doc (PR merge state for the remaining
  un-checked items, the broader home-directory worktree/backup sweep, "deleted gemma
  manually") still stand as originally written except where explicitly answered
  above.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-17T20:52Z | ALIVE (investigation+additive-merge pass complete) | n/a (doc only, untracked) | read-only git/ls/du + additive commits/pushes only; zero deletions | Still Open list above |
| 2026-09-17T21:00Z | ALIVE | release/v26.9.17 (pre-commit) | milestone captured into git as part of v26.9.17 release; correction: PR #267 was reported MERGED here but `git merge-base --is-ancestor 7e62e475 origin/main` is false — fix never landed on main; superseded by the ggen.toml comment correction + lock-contracts tripwire in the v26.9.17 release | Still Open list above (deletion pass, docs/capture PR decision, key rotation) |
