# Branch protection — proposed, not yet applied

`.github/rulesets/main-branch-protection.json` is a real, ready-to-apply
GitHub ruleset for `main`. It is **deliberately not applied yet**.

## Why not applied now

At the time this was written, multiple automation swarms
(`automation/ws1-*`, `automation/ws2-*`, `automation/ws4-*` branches) were
actively merging directly to `main` via PRs on a short cadence. Turning on
`required_status_checks` against the `Deterministic ecosystem manufacture`
check right now would block those in-flight merges the moment any one of
them lands without that check having run cleanly first, and there was no
coordinated moment to verify all active swarms would clear it. Applying a
protection rule is a repository-wide behavior change, not a reversible
local edit — it needs a deliberate go/no-go, not a unilateral flip mid-swarm.

## What the ruleset does

- Blocks branch deletion and non-fast-forward pushes to `main`.
- Requires the `Deterministic ecosystem manufacture` status check
  (from `.github/workflows/ggen-ecosystem-sync.yml`) to pass before merge.
- Bypass actor for repository admins is included so the repo owner is never
  locked out — **the exact numeric `actor_id` (5) for the admin
  `RepositoryRole` is per GitHub's documented rulesets schema but has not
  been test-applied against this specific repo; verify it resolves to
  "Admin" (not another role) before applying, e.g. via the ruleset editor
  UI at Settings → Rules → Rulesets → New ruleset, which will echo back the
  resolved role name.**

## How to apply

Once ready (all active automation swarms coordinated or paused):

```bash
# Strip the _comment key first -- GitHub's API rejects unknown properties
python3 -c "import json; d=json.load(open('.github/rulesets/main-branch-protection.json')); d.pop('_comment', None); print(json.dumps(d))" \
  | gh api --method POST repos/seanchatmangpt/ggen-ecosystem/rulesets --input -
```

Or via the UI: Settings → Rules → Rulesets → New branch ruleset, and
transcribe the same conditions/rules (safer for a first application, since
the UI validates the bypass actor role interactively).
