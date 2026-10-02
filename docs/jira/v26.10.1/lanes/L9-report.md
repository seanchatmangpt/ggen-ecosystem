# L9 report — pre-bump court baseline + integration checklist (v26.10.1)

## Lane

- Lane: L9 (baseline receipts + integration checklist; owned files `receipts/v26.10.1/*` + this report)
- Subject: branch `release/v26.10.1` @ `19a2b1f1` (first action verified: `git rev-parse --abbrev-ref HEAD` → `release/v26.10.1`, `git rev-parse --short HEAD` → `19a2b1f1`)
- Date: 2026-10-01
- Standing: **ALIVE** for the court baseline (observed execution of `lock_crown_court.py` against subject `19a2b1f1` with exit 0 / ALIVE / 0 violations); **REFUSED_NO_DRYRUN** for the crown dry-run (contract-prescribed); checklist is a written deliverable (STATIC, not executed end-to-end — its commands were individually probe-verified, noted per step).

## Files written (all left UNSTAGED — no `git add`, zero git state commands)

1. `receipts/v26.10.1/prebump-lock-crown-court.json` — court baseline envelope (PASS)
2. `receipts/v26.10.1/prebump-crown-dryrun.json` — crown dry-run attempt envelope (REFUSED_NO_DRYRUN)
3. `receipts/v26.10.1/prebump-court-python39-attempt.txt` — the failed ambient-`python3` invocation (evidence for the 3.11+ requirement) + interpreter census
4. `receipts/v26.10.1/integration-court-checklist.md` — ordered integration commands with expected outcomes + failure meanings
5. `docs/jira/v26.10.1/lanes/L9-report.md` — this report (contracted deliverable)

Scratch: `/tmp/v26101-lane9/` (`lock-at-T0.toml`, `court-stdout.txt`, `court-stderr.txt`, `crown-help.txt`). Nothing else created or modified in the repo. `ecosystem.lock.toml`, `RESOLUTIONS.md`, `vendor/*` read-only, never written.

## Commands + exits (chronological; all run 2026-10-01)

| # | command | exit | result |
|---|---|---|---|
| 1 | `git rev-parse --abbrev-ref HEAD && git rev-parse --short HEAD` | 0 | `release/v26.10.1`, `19a2b1f1` |
| 2 | T0 baseline capture: `git status/diff --stat ecosystem.lock.toml`, `shasum -a 256`, snapshot to scratch | 0 | lock clean vs HEAD, sha256 `d6bc2edc…`, T0=19:25:56Z |
| 3 | `ls scripts/ \| grep -iE 'crown\|court\|lock'` | 0 | `crown-submodules.py`, `lock_crown_court.py`, `qme_crown.py` |
| 4 | `python3 scripts/lock_crown_court.py --help` | **1** | `ModuleNotFoundError: No module named 'tomllib'` (python3 = 3.9.6) → recorded in `prebump-court-python39-attempt.txt` |
| 5 | `python3 scripts/crown-submodules.py --help` | 0 | flags: `--apply`, `--receipt` only — no dry-run form |
| 6 | `python3.11 scripts/lock_crown_court.py` (default `--rev HEAD`) | **0** | stdout JSON: `standing: ALIVE`, `violations: []`, `subject: 19a2b1f1467dc7820ca0704e99507aa68e676259`, t=19:28:47Z→19:28:48Z → receipt #1, interpretation PASS |
| 7 | `git submodule status` | 0 | all six `+`-prefixed at old WIP checkouts (d5ac60ff, 57436870, 06093e0c, 616e93d1, d84da141, da48e98c) |
| 8 | `which ggen && ggen --version` | 0 | `/Users/sac/.local/bin/ggen`, `ggen 26.9.28` |
| 9 | stale-pin grep snapshot (v26.9.25-era strings) | 0 | pre-bump hits recorded: lock v26.8.27/v26.9.29-era identity, README:13/:86, CURRENT-RELEASE-STANDING:10 `2c4c4c7e…`, TRANSPORT narrative |
| 10 | interleaving re-checks T1/T2/T3: `git diff --stat ecosystem.lock.toml` + sha256 | 0 | lock sha256 `d6bc2edc…` UNCHANGED 19:25:56Z → 19:39:41Z — L1 had NOT landed during my window |
| 11 | `git ls-tree HEAD -- vendor/` vs `git ls-tree dc665a1e -- vendor/` | 0 | recorded gitlinks at BOTH revs already == RESOLUTIONS targets, all six |
| 12 | `git merge-base --is-ancestor dc665a1e HEAD` | 0 | base IS ancestor of HEAD |
| 13 | `python3.11 -c "import yaml/rdflib"` probes; `ggen sync --help`; `command -v rapper` | 0 | yaml OK, rdflib OK, `ggen sync` usage confirmed, rapper present — checklist commands verified runnable |

## Decisions + rationale

**D1 — Baseline validity despite concurrent lanes (interleaving handled per contract).**
Contract required early capture because L1 edits `ecosystem.lock.toml` concurrently. Evidence: lock sha256 `d6bc2edc…` identical at T0 19:25:56Z / T1 / T2 19:32:54Z / T3 19:39:41Z; `git diff` vs HEAD empty throughout. The court's ALIVE verdict at 19:28:47Z additionally proves workflow+ontology+CHANGELOG were still pre-bump-coherent at that moment — the court reads those from the worktree (court lines 249/267–269), and any mid-bump state against the v26.9.29 lock would have raised WORKFLOW_CONTAINER_TAG / PROJECTION_PARITY / MARKETPLACE_DEFAULT_UNRECORDED / RELEASE_UNRECORDED. L4's flip to v26.10.1/`bf9eccb3…` was observed landed between 19:29Z and 19:31Z (after my court run). Interleaving recorded inside the receipt JSON.

**D2 — `REFUSED_NO_DRYRUN` stands even though the bare form is plan-only.**
No `--dry-run/--check/--diff` flag exists (`--help`: only `--apply`, `--receipt`), so per contract I did not execute the script beyond `--help`. Static read (crown-submodules.py `main()`/`plan()`/`apply()`) shows the contract's rationale ("would mutate gitlinks") is true only for `--apply`; the bare form is read-only for the repo but still not side-effect-free: it runs `git ls-remote --symref` against all six vendor remotes and writes a receipt JSON defaulting to `artifacts/autonomic-crown.json` (outside my owned path). Recorded in the receipt as source-read evidence so the coordinator can use the bare form as its step-2 plan check.

**D3 — Hazard: `crown-submodules.py --apply` crowns to REMOTE heads, not RESOLUTIONS targets.**
`apply()` uses `remote_head()` (ls-remote) as the crown target and `replace_exact_sha(old→new)` on the lock, refusing `CROWN_BLOCKED[LOCK_PIN_NOT_FOUND]` on zero hits. The checklist therefore gates `--apply` behind a read-only plan comparison against RESOLUTIONS.md: any remote drift past the pinned targets = STOP (seam conflict), and with recorded gitlinks already at targets the expected `changed_count` is 0 → the correct integration action is materialization (`git submodule update --init`), not `--apply`.

**D4 — Discovered: the "crown to targets" is already done in the recorded tree.**
`git ls-tree HEAD -- vendor/` and at base `dc665a1e` both show all six recorded gitlinks EXACTLY equal to the RESOLUTIONS targets (autofde `71de04a6…`, beam4pm `7bad16ab…`, ggen `ff96f04e…`, marketplace `bf9eccb3…`, igniter `0abed8a3…`, wasm4pm `a7352d81…`); the lock `[submodules]` and per-producer sections agree. Only worktree checkouts lag (all `+` at old WIP SHAs). This is why the pre-bump court passes with 0 violations (`GITLINK_PIN`/`SECTION_PIN` compare rev-read gitlinks vs lock). Integration's crown step reduces to checkout materialization + verification.

**D5 — Two predicted court REFUSALS in the pinned seams as written (flagged, not fixed — not L9 seams).**
(a) **RELEASE_IDENTITY** (court lines 171–173, unconditional `[container].tag == [ggen].release`): RESOLUTIONS pins tag `v26.10.1` while recommending `[ggen].release` option (a) `v26.9.28` → court exit 1. The chain WORKFLOW_CONTAINER_TAG (workflow default already `v26.10.1`) + RELEASE_UNRECORDED (L3 writes `## [v26.10.1]`) forces release = `v26.10.1`; option (a) as-written is court-inconsistent. Cross-check: L1's delegated decision remains L1's — flagged for L1/coordinator resolution BEFORE the final court.
(b) **UPDATED_AT_STALE** (court lines 222–226; fires when `updated_at + 300s < base_main_sha` commit time): RESOLUTIONS pins `updated_at = 2026-10-01T00:00:00Z` but the new `base_main_sha = dc665a1e` was committed **2026-10-01T19:11:18Z** → the pinned stamp would refuse. Lawful window: `≥ 19:11:18Z` and `≤ release-commit time` (mirror law UPDATED_AT_FUTURE). Note the crown's `updated_at := now()` overwrite only fires when `changed_count > 0`, which D3/D4 make unlikely — do not rely on it.
Both are recorded in the checklist's "TWO PREDICTED COURT REFUSALS" section with source line numbers and a pre-commit sanity snippet (checklist step 4) that names them before a full court run.

**D6 — Court sequencing law: run the final court on the COMMITTED tree.**
The court reads gitlinks from the rev (`git ls-tree <subject>`, court line 243) but lock/workflow/ontology/CHANGELOG from the worktree. Pre-commit runs produce false GITLINK_PIN refusals. Checklist step 5 orders: commit → court.

**D7 — Interpreter pin.**
Court requires `tomllib` (3.11+); ambient `python3` is 3.9.6 (failed invocation preserved). All checklist commands pinned to `python3.11` (3.11.6 witnessed). Also witnessed working: python3.11 `yaml`, python3.11 `rdflib`, `ggen` 26.9.28, `rapper`.

**D8 — From-value drift (corroborates L4's D1/D2, independent observation).**
RESOLUTIONS describes pre-state pins as v26.9.25-era (`2c4c4c7e…`), but the repo sat at v26.9.29-era (`637b561c…`, base `38ccda68…`) before this milestone. Affects only prose accuracy of RESOLUTIONS; targets are unaffected. Also noted as data for L1: RESOLUTIONS says "latest asset-bearing ggen release is v26.9.28" while the lock records `latest_published_release = "v26.9.29"` / sha `637b561c…` — the [ggen].release evidence base is internally inconsistent and needs L1's resolution either way.

## REFUSED / BLOCKED / UNKNOWN items

- **REFUSED_NO_DRYRUN** — crown dry-run: no dry-run flag exists; script not executed beyond `--help` (evidence in receipt #2). Contract-prescribed refusal, not a lane failure.
- **REFUSED (predicted, pre-integration)** — RELEASE_IDENTITY and UPDATED_AT_STALE if the RESOLUTIONS seams land exactly as pinned (D5). Owner: L1/coordinator. Not fired at baseline (baseline court is ALIVE).
- **BLOCKED (none)** — nothing blocked L9's own work.
- **UNKNOWN** — (1) whether remote vendor heads still equal the RESOLUTIONS targets at integration time (L9 did not ls-remote; that probe is checklist step 2 and coordinator-owned since `--apply` is); (2) whether L1's eventual `[ggen].release` value satisfies RELEASE_IDENTITY (L1 had not landed by 19:39:41Z); (3) `ggen sync` regen behavior against the new marketplace pin (requires coordinator run after materialization; checklist step 8).
- **Falsifier attempted** — tried to invalidate my own baseline by checking whether concurrent edits had contaminated it: sha256 chain T0→T3 unchanged + court reader-semantics analysis + verdict coherence argument (D1). Baseline survives.

## Addendum (19:46:35Z — post-baseline, pre-close observation)

L1's lock edit landed at ~19:44Z (after all L9 captures; baseline court unaffected — lock was byte-identical to HEAD from 19:25:56Z through 19:39:41Z, court ran 19:28:47Z). Diff vs HEAD (`git diff HEAD -- ecosystem.lock.toml`, 11 ins / 11 del) observed read-only at 19:46:35Z:

- **R2 (UPDATED_AT_STALE): RESOLVED by L1.** `updated_at = "2026-10-01T19:44:09Z"` (wall-clock, inside the lawful window ≥ base `dc665a1e` @ 19:11:18Z). `base_main_sha = "dc665a1e…"` as pinned.
- **R1 (RELEASE_IDENTITY): LIVE — the court WILL refuse the tree as it now stands.** Landed: `[ggen].release = "v26.9.28"` (RESOLUTIONS option (a)) with `[container].tag = "v26.10.1"`. Court lines 171–173 are unconditional: `tag != release` → `RELEASE_IDENTITY`, exit 1. Additionally `RELEASE_UNRECORDED` will fire unless CHANGELOG carries a `## [v26.9.28]` section (L3's entry is `## [v26.10.1]`), and `WORKFLOW_CONTAINER_TAG` stays satisfied only by tag `v26.10.1` (L4 landed the workflow defaults at `v26.10.1`).
- Consequence: with the landed combination, `python3.11 scripts/lock_crown_court.py` at integration exits 1 with at least `RELEASE_IDENTITY` (+ likely `RELEASE_UNRECORDED`). The two court-consistent exits remain as in the checklist (release = tag = `v26.10.1`, or coordinator revises both seams to the same value). Resolution belongs to L1/coordinator — L9 owns no lock byte and changes none.
- New data point for L1's evidence base: landed `latest_published_release = "v26.9.30"` / sha `80d429f1…` — supersedes both the "v26.9.28 latest asset-bearing" RESOLUTIONS fact and the pre-bump lock's `v26.9.29`/`637b561c…` values (D8's inconsistency now has a third observed state; `[ggen].release = v26.9.28` sits below the lock's own latest-published value).
