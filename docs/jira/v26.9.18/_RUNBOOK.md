# _RUNBOOK — dispatch prompt canonical form (v26.9.18 wave)

Every agent in this wave receives EXACTLY this prompt shape, filled in:

```
You are implementing one ticket in a 15-agent wave for RFC-GPACK-001
(the GGEN Semantic Pack Protocol).

TICKET (read it first, obey its History table law): <ticket path>
RFC (the spec you implement; cite sections in your commit message):
  /Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md
WORKTREE (your only write surface): <worktree path>
REPO LAWS: <worktree>/AGENTS.md (read before writing)

Rules:
1. Work ONLY inside the worktree. Never push. Never touch other worktrees,
   the main checkouts, or any remote.
2. Commit to the pre-created branch with conventional-commit messages.
3. Run the repo's own tests for your changed scope; paste real command +
   exit code into the ticket History. No test = no done.
4. Every normative claim you implement gets its falsifier (a test) in the
   same change. A guard that cannot fail is vacuous — prove it can.
5. Preserve legacy behavior exactly as the ticket says; this RFC is
   compatibility-preserving by construction (§85/§86/§88/§89).
6. Append one History row (ts | standing | branch+SHA | gates+exits |
   remaining) for every transition. Final row claims a standing from
   {ALIVE, PARTIAL_ALIVE, BLOCKED, BUILD_BROKEN, REFUSED_*, UNKNOWN}.
   ALIVE requires observed test execution in this session.
7. If blocked >2 attempts on one error: stop, record BLOCKED + the exact
   diagnostic, leave the tree committed.
8. Out-of-scope items in the ticket are law. Silent pruning forbidden —
   record any edge you did not take and why.
```

Integration (coordinator-only, serialized per repo, ONE --no-ff merge per
integration pass, diff-reviewed + test-gated; red → reset + BLOCKED + reopen):
see PLAN.md §Integration.
