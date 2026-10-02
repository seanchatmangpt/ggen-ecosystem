# L7 lane report — ecosystem.ttl version crown + TRANSPORT

- lane: L7
- subject: branch `release/v26.10.1` @ `19a2b1f1` (base `dc665a1e` verified ancestor, exit 0)
- files-written (all left UNSTAGED, no `git add` run):
  - `ecosystem.ttl` — modified (1 line)
  - `docs/TRANSPORT.md` — modified (1 line, on top of preserved WIP, kept)
  - `docs/jira/v26.10.1/lanes/L7-report.md` — created (this report)

## Decisions + rationale

1. `ecosystem.ttl` line 12: `dcterms:hasVersion "26.8.27"` → `"26.10.1"`.
   - Seam from RESOLUTIONS.md ("Derived pins") matches observed file content exactly → no seam conflict.
   - Grounding: `CHANGELOG.md` `[Unreleased]` note (lines 17-20) records the hasVersion-vs-lock lag as
     intentional "until the next crown bumps it"; this crown is that event (milestone v26.10.1, 2026-10-01).
   - Style check (`sed -n '1,30p'`): the file is plain turtle with zero comments (all `grep '#'` hits are
     `https://...#` URI fragments), so no rationale-comment pattern exists → changed only the literal
     (minimal diff, per contract).
   - Other version-bearing literals: `grep -nE 'v26\.|26\.[0-9]' ecosystem.ttl` pre-edit matched ONLY line 12
     — no other version literals exist, so nothing to flag UNKNOWN, nothing else changed.
2. `docs/TRANSPORT.md` line 7: crown-of-the-moment identity updated v26.9.25 → v26.10.1.
   - Changed: "as of the v26.9.25 crown (2026-09-26)" → "as of the v26.10.1 crown (2026-10-01)";
     "awaiting-publish state for tag `v26.9.25`" → "...for tag `v26.10.1`"; "the v26.9.25 image has not
     yet been published, pulled, and consumer-executed" → "the v26.10.1 image ...". Per RESOLUTIONS.md
     pinned seam `[container].tag` → `v26.10.1`, standing `BLOCKED`, `requires_republish = true`.
   - Kept intact (preserved WIP, per contract):
     - the WIP correction itself (the line-7 rewrite is the uncommitted WIP — `git diff` pre-edit confirmed
       the working-tree change was exactly this sentence's v26.9.25-era update);
     - "the pinned digest still describes the v26.9.22-era image" — factual descriptor of the digest, not a
       crown ref; grounded: `ecosystem.lock.toml` `[container]` (clean at HEAD `dc665a1e`-line and working
       tree) records `requires_republish = true` through the v26.9.29 crown with failure "digest below is
       historical evidence from the prior published image" and last `observed_success_at 2026-09-23T08:27:01Z`
       (run 35833887166) — no republish recorded since;
     - "(Historical root-cause note, 2026-08-29: ... Actions run `33238309149` ...)" — past receipt, intact.
   - Release-identity sweep: `grep -nE 'v26\.[0-9]|[0-9a-f]{40}' docs/TRANSPORT.md` matched line 7 only
     (no 40-hex SHA references anywhere in the file; line 5 carries no version refs). Not a NO-OP — one
     crown-of-record sentence updated; every change itemized above and in the diff.

## Commands + exits (all run in /Users/sac/ggen-ecosystem)

| # | command | exit | result |
|---|---|---|---|
| 1 | `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 | `release/v26.10.1`, `19a2b1f1` |
| 2 | `git merge-base --is-ancestor dc665a1e9357... HEAD` | 0 | base is ancestor of HEAD |
| 3 | `git status --porcelain -- ecosystem.ttl docs/TRANSPORT.md` | 0 | `M docs/TRANSPORT.md` (preserved WIP), ttl clean |
| 4 | `sed -n '1,30p' ecosystem.ttl` | 0 | plain turtle, no comment pattern |
| 5 | `grep -nE 'v26\.|26\.[0-9]' ecosystem.ttl` | 0 | only line 12 `dcterms:hasVersion "26.8.27"` |
| 6 | `grep -n '#' ecosystem.ttl` | 0 | only URI-scheme fragments, no comments |
| 7 | `grep -n -A3 -B3 'hasVersion' CHANGELOG.md` | 0 | grounding note, lines 17-20 |
| 8 | `grep -nE 'v26\.[0-9]|[0-9a-f]{40}' docs/TRANSPORT.md` | 0 | line 7 only; zero 40-hex SHAs |
| 9 | `git show HEAD:ecosystem.lock.toml` + `sed -n '/\[container\]/,/^\[/p' ecosystem.lock.toml` (both) | 0 | tag `v26.9.29`, `BLOCKED`, `requires_republish = true`, failure cites digest as historical evidence; `observed_success_at` 2026-09-23 |
| 10 | `git status --porcelain ecosystem.lock.toml` | 0 | clean (shared-read, L1-owned — not modified by this lane) |
| 11 | `git diff docs/TRANSPORT.md` (pre-edit) | 0 | WIP = the line-7 v26.9.25-era rewrite itself |
| 12 | post-edit `grep -n 'hasVersion' ecosystem.ttl`; `grep -nE 'v26\.[0-9]|...' docs/TRANSPORT.md`; `git diff ecosystem.ttl` | 0 | edits verified on disk, unstaged |

## REFUSED / BLOCKED / UNKNOWN items

- REFUSED: none. No seam conflicts — every pinned value used agreed with observed evidence.
- BLOCKED: the transport standing recorded in TRANSPORT.md remains `BLOCKED` (`requires_republish = true`) —
  the v26.10.1 image is not yet published/pulled/consumer-executed. This is the documented state, not a lane
  failure. Lane deliverable standing: complete (both owned files updated, verified by diff/grep, left unstaged).
- UNKNOWN: `ecosystem.lock.toml` at dispatch carries `[container].tag = "v26.9.29"` — an intermediate crown
  (between v26.9.25 and v26.10.1) that TRANSPORT.md never mentioned. Not added to TRANSPORT.md (minimal diff;
  the lock itself remains "the exact record of this transport's current standing" that the doc points readers
  to, and L1's pinned seam writes `v26.10.1` over it at integration). Flagged here so the coordinator sees the
  v26.9.29 interlude exists in lock history.
- Note: inspection ≠ execution — the ttl literal and the prose were text edits verified by diff/grep; no
  pipeline, tag, or container publication was executed by this lane (coordinator-owned at integration).
