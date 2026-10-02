# L4 report — sync workflow + ontology pin bump (v26.10.1)

## Lane

- Lane: L4 (`.github/workflows/ggen-ecosystem-sync.yml`, `ontology.ttl` only)
- Subject: branch `release/v26.10.1` @ `19a2b1f1` (verified first action: `git rev-parse --abbrev-ref HEAD` / `--short HEAD`)
- Date: 2026-10-01
- Standing: files bumped + statically validated (grep/parse/diff gates below). Workflow execution with the new defaults is UNKNOWN until a real dispatch; a default-tag dispatch additionally requires the `v26.10.1` container image to exist — RESOLUTIONS pins `[container].tag` standing `BLOCKED` / `requires_republish = true`, so this is expected release sequencing, not a lane defect.

## Files written (all left UNSTAGED — no git add, no git state commands)

1. `.github/workflows/ggen-ecosystem-sync.yml` — 4 value lines
2. `ontology.ttl` — 4 value lines
3. `docs/jira/v26.10.1/lanes/L4-report.md` — this report (contracted deliverable)

Scratch: `/tmp/v26101-lane4/` (`evidence-pre.txt`, `evidence-post.txt`). Nothing else created or modified in the repo.

## The bump actually applied

| pin | from (observed on disk) | to (RESOLUTIONS-pinned target) | spots per file |
|---|---|---|---|
| `ggen_container_tag` default | `v26.9.29` | `v26.10.1` | 2 |
| `marketplace_sha` default | `637b561cc6384fc9ac0e4282d048cc7624256258` | `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2` | 2 |

Spots: workflow lines 11/16 (workflow_call) + 38/43 (workflow_dispatch); ontology.ttl lines 25/30 (`gha:onBlock` workflow_call block) + 52/57 (workflow_dispatch block).

## Decisions + rationale

**D1 — Bumped from `v26.9.29`/`637b561c…`, not the contracted `v26.9.25`/`2c4c4c7e…`.**
The contract and RESOLUTIONS.md describe the from-values as `v26.9.25` / `2c4c4c7e2a4eb33ebe2ad9ab23725af3c476a637`. Pre-edit evidence: those strings have **zero occurrences** in either owned file at HEAD (`grep -rn 'v26\.9\.25\|2c4c4c7e' …` → exit 1). `git log -S` shows they existed at `3b75fe27` ("release: bump to v26.9.25") and were replaced at `caaad47d` ("feat(release): project v26.9.29 immutable release defaults", mirrored by `9b3e4e64`) — the repo already sits at v26.9.29-era pins. The observed pins are the same pin kinds at exactly the contracted positions (2 tag defaults + 2 marketplace_sha defaults per file), so the contract's clause "other stale v26.x pins: bump if they are the same tag/marketplace_sha pins" governs. Bumped to the pinned targets.

**D2 — Not classified REFUSED_SEAM_CONFLICT.**
The refusal clause guards seam values a lane is told to *write*. Every value I wrote (`v26.10.1`, `bf9eccb3…`) is exactly the RESOLUTIONS.md pinned target and agrees with the pinned crown target for ggen-marketplace. What drifted is the coordinator's description of the *pre-state* (stale v26.9.25-era from-values), not any target seam. Flagged as UNKNOWN-F1 below for L10/coordinator instead. Leaving the files unchanged would have produced a worse end state: defaults contradicting the repo's own gitlink (see D3).

**D3 — Target `bf9eccb3…` verified against the repo's own submodule state, not just RESOLUTIONS.md.**
`git ls-tree HEAD vendor/ggen-marketplace` → gitlink is **already** `bf9eccb3420134d4850dd49a5cbbef7dc35f20e2` at this HEAD; `git -C vendor/ggen-marketplace rev-parse --verify 'bf9eccb3…^{commit}'` resolves; commit metadata: 2026-09-30 "Merge branch 'feat/ex4pm-pack-upgrade-v26.9.30' into main" — consistent with RESOLUTIONS "origin/main, describes v26.9.30-6-gbf9eccb34". The workflow input's own invariant ("must match vendor/ggen-marketplace submodule pin") is therefore TRUE post-bump; the old default `637b561c…` ("release: bump marketplace version to v26.9.29", 2026-09-28) contradicted the gitlink and would have driven `REFUSED[MARKETPLACE_SUBMODULE_DRIFT]` semantics on default runs.

**D4 — Zero reformatting.** Value-only substitution; `git diff -U0` shows exactly 2 del + 2 ins per file, line positions unchanged (workflow 11/16/38/43, ontology 25/30/52/57), total 8 changed lines across both files.

**D5 — No other stale v26.x pins found.** Broad grep `v26\.` over both files pre-edit: workflow lines 11/38 only; ontology lines 25/52 only. Nothing else to bump; nothing flagged out of the "other stale pins" clause.

## Commands + exits (full logs: `/tmp/v26101-lane4/evidence-pre.txt`, `evidence-post.txt`)

| command | exit | result |
|---|---|---|
| `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 | `release/v26.10.1` / `19a2b1f1` |
| `grep -n 'v26\.9\.25\|2c4c4c7e' .github/workflows/ggen-ecosystem-sync.yml` | 1 | empty — contracted from-values absent |
| `grep -n 'v26\.9\.25\|2c4c4c7e\|v26\.' ontology.ttl` | 0 | only `default: v26.9.29` at 25/52 |
| `grep -n 'v26\.' .github/workflows/ggen-ecosystem-sync.yml` | 0 | only 11/38 |
| `grep -n '637b561c' <both files>` | 0 | 2 per file (16/43, 30/57) |
| `git ls-tree HEAD vendor/ggen-marketplace` | 0 | gitlink already `bf9eccb3…` |
| `git log -S '637b561c' / -S '2c4c4c7e' / -S 'v26.9.25' -- <owned files>` | 0 | `caaad47d`/`9b3e4e64` replaced v26.9.25-era pins (drift classification) |
| `git -C vendor/ggen-marketplace rev-parse --verify 'bf9eccb3…^{commit}'` | 0 | target SHA reachable locally |
| `git -C vendor/ggen-marketplace log -1 … bf9eccb3` / `637b561c` | 0 | 2026-09-30 merge / 2026-09-29 v26.9.29 bump |
| post: `grep -rn 'v26\.9\.25\|2c4c4c7e' <both files>` | 1 | empty — contract after-check PASS |
| post: `grep -rn 'v26\.9\.29\|637b561c' <both files>` | 1 | empty — old values gone |
| post: `grep -c 'default: v26\.10\.1' / 'default: bf9eccb3…' <both files>` | 0 | 2 + 2 per file |
| post: `python3 -c "yaml.safe_load(open('.github/workflows/ggen-ecosystem-sync.yml'))"` | 0 | `YAML_PARSE_OK` |
| post: `python3 -c "rdflib.Graph().parse('ontology.ttl', format='turtle')"` | 0 | `TURTLE_PARSE_OK` (241 triples) |
| post: `git diff -U0 -- <both files>` | 0 | exactly the 8 pin lines, nothing else |
| post: `git status --porcelain -- <both files>` | 0 | ` M` both — modified, UNSTAGED |

## REFUSED / BLOCKED / UNKNOWN items

- **REFUSED**: none. **BLOCKED**: none at lane scope (container-image republish BLOCKED is coordinator-owned and already pinned in RESOLUTIONS).
- **UNKNOWN-F1 (RESOLUTIONS/contract from-value drift, action: none by this lane)**: both documents state the current pins as `v26.9.25`/`2c4c4c7e…`; observed reality at HEAD is `v26.9.29`/`637b561c…` (evidence in D1). Targets were unaffected and are now landed. Coordinator may want RESOLUTIONS.md corrected or a note appended; L10's seam audit will see final state `v26.10.1`/`bf9eccb3…`.
- **UNKNOWN-F2 (pre-existing generated-vs-ontology action-pin drift, action: left untouched — outside pin scope)**: the workflow YAML (marked GENERATED from this ontology) pins `actions/checkout@3d3c42e5 # v7.0.1`, `actions/cache@55cc8345 # v6.1.0`, `actions/upload-artifact@043fb46d # v7.0.1`, while `ontology.ttl` facts still record `checkout@d23441a4 # v6`, `cache@caa29612 # v5`, `upload-artifact@b7c566a7 # v6` (ex:checkout/ex:cache/ex:upload). A future `ggen sync run` regeneration from ontology.ttl would revert those action pins backward. Coordinator decision; not a pin this lane owns.

## Receipt notes

- Generated vs hand-written: 8 pin-value lines changed by targeted substitution (μ = edit of generated/ontology artifacts at their pinned seams); report manufactured. Operator hand-wrote nothing.
- Falsifiers attempted: (a) absence greps for both the contracted stale values and the actual old values post-edit (both exit 1 = absent); (b) parse gates for YAML and Turtle; (c) `git diff -U0` mutation check proving value-only change; (d) target-SHA reachability in the exact submodule the workflow validates against. All survived.
