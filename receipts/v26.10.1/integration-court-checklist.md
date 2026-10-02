# v26.10.1 Integration Court Checklist (L9)

Computed 2026-10-01 by L9 from the pre-bump baseline (`receipts/v26.10.1/prebump-lock-crown-court.json`,
court ALIVE 0 violations on subject `19a2b1f1`) plus a static read of `scripts/lock_crown_court.py`
and `scripts/crown-submodules.py`. Every command below was verified runnable at baseline
(interpreter probes in `prebump-court-python39-attempt.txt`).

## 0. Interpreter precondition

```bash
python3.11 --version   # expect 3.11.x (baseline: 3.11.6 at /usr/local/bin/python3.11)
```

The court imports `tomllib` (3.11+ stdlib). Ambient `python3` is 3.9.6 and fails with
`ModuleNotFoundError: No module named 'tomllib'` (exit 1) — witnessed at baseline. Use
`python3.11` for every step below.

## Baseline facts this checklist is conditioned on (all witnessed 2026-10-01T19:25–19:40Z)

- Recorded gitlinks at HEAD `19a2b1f1` ALREADY EQUAL the RESOLUTIONS.md targets
  (`git ls-tree HEAD -- vendor/` == targets; also true at base `dc665a1e`). Only the worktree
  submodule checkouts lag (all six show `+` at old WIP SHAs d5ac60ff/57436870/06093e0c/
  616e93d1/d84da141/da48e98c). The "crown to targets" step is therefore mostly a
  materialization step, not a pin move.
- `ecosystem.lock.toml` at HEAD is ALREADY target-consistent in `[submodules]` and all
  per-producer `sha`/`commit_sha` fields; what still moves is: `base_main_sha`
  (38ccda68… → dc665a1e…), `[ggen].release` (v26.9.29), `[container].tag` (v26.9.29),
  `updated_at`, and CHANGELOG/release narrative.
- `ontology.ttl` + `ggen-ecosystem-sync.yml` defaults already flipped to
  `v26.10.1` / `bf9eccb3…` in the worktree by L4 (observed 19:31Z).

## TWO PREDICTED COURT REFUSALS in the pinned seams as written — resolve BEFORE the final court

### R1: RELEASE_IDENTITY (`lock_crown_court.py` lines 171–173, unconditional)

```python
tag = container.get("tag")
if tag != release:  # -> ("RELEASE_IDENTITY", ...)
```

RESOLUTIONS pins `[container].tag = v26.10.1` while delegating `[ggen].release` to L1 with
recommended option (a) `v26.9.28`. If L1 lands (a) as-is, the final court REFUSES
(`RELEASE_IDENTITY`, exit 1). The court chain also forces release = v26.10.1:
WORKFLOW_CONTAINER_TAG requires workflow default (already v26.10.1) == `[container].tag`, and
RELEASE_UNRECORDED requires a `## [<release>]` CHANGELOG section (L3 writes `## [v26.10.1]`).
Only court-consistent combos: `[ggen].release = v26.10.1` **and** `[container].tag = v26.10.1`
(tag-pin + typed BLOCKED note for missing assets = RESOLUTIONS option (b) shape, at v26.10.1),
or the coordinator explicitly revises both seams to the same other value.

### R2: UPDATED_AT_STALE (`lock_crown_court.py` lines 222–226)

Fires when `updated_at + 300s < base_main_sha` commit time. RESOLUTIONS pins
`updated_at = 2026-10-01T00:00:00Z`, but the new `base_main_sha = dc665a1e` was committed
**2026-10-01T19:11:18Z**. `00:00:00Z + 300s < 19:11:18Z` → REFUSED. Lawful window for
`updated_at`: `>= 2026-10-01T19:11:18Z` and `<= release-commit time` (UPDATED_AT_FUTURE is the
mirror law). Writing the wall-clock stamp at integration satisfies both. Note: crown
`--apply` overwrites `updated_at` with `now()` only when `changed_count > 0` — do not rely on
that (see step 2 decision table: with gitlinks already at targets the expected
`changed_count` is 0 and NO rewrite happens).

Neither R1 nor R2 is an L9 seam — flagged `REFUSED_SEAM_CONFLICT`-equivalent for L1/coordinator;
seams left unchanged by L9.

## Ordered integration steps (coordinator only; each: command → expected → failure meaning)

### 1. Confirm all lanes landed

```bash
git status --short                 # expect clean except intended integration outputs
git log --oneline dc665a1e..HEAD   # expect per-lane atomic commits present
```
Uncommitted lane files here means integration started early — stop, land lanes first.

### 2. Crown plan check — READ-ONLY, decide before any apply

```bash
python3 scripts/crown-submodules.py --receipt /tmp/v26101-crown-plan.json | python3.11 -c "import json,sys; d=json.load(sys.stdin); [print(r['path'], r['current'], r['latest']) for r in d['submodules']]; print('changed_count', d['changed_count'])"
```
Expected: every `latest` EXACTLY equals its RESOLUTIONS.md target, `current` equals the same
(recorded gitlinks are already at targets), `changed_count = 0`.

Decision table:

| plan state | action |
|---|---|
| all `latest` == targets, changed_count = 0 | **Do NOT run `--apply`.** Nothing to crown. Go to step 3. |
| any `latest` != target | **STOP — do NOT `--apply`.** `apply()` crowns to the REMOTE head (`git ls-remote`), never to RESOLUTIONS.md; it would move gitlinks and rewrite lock pins PAST the pinned seams (exact-match replace of the target SHA). That is a seam conflict with RESOLUTIONS.md → coordinator re-resolves seams first. |
| `CROWN_BLOCKED[LOCK_PIN_NOT_FOUND]` | means a lock `[submodules]` commit no longer matches its recorded gitlink — lanes/coordinator moved one without the other; reconcile by hand at the RESOLUTIONS values. |

Rationale: `apply()` = `git submodule update --init --depth 1` + `git fetch --depth 1` +
`git checkout --detach <remote-head>` per changed vendor + exact-match SHA replace in
`ecosystem.lock.toml` + `updated_at := now()` (crown-submodules.py lines 108–127). With
changed_count = 0 it is a no-op that only writes a receipt — skipping it is correct, not a
shortcut.

### 3. Materialize worktree checkouts to the recorded pins

```bash
git submodule update --init        # coordinator-only git state command
git status --short -- vendor/      # expect EMPTY (no M entries)
git submodule status               # expect all six space-prefixed (no + / - / U)
```
Failure meaning: a vendor cannot fetch/checkout its pinned SHA → remote history problem;
resolve before committing, never by re-pointing the pin.

### 4. Pre-commit lock sanity (fast rejection of R1/R2 without a full court run)

```bash
python3.11 - <<'EOF'
import tomllib
lock = tomllib.load(open("ecosystem.lock.toml","rb"))
assert lock["container"]["tag"] == lock["ggen"]["release"], "R1 RELEASE_IDENTITY would fire"
assert lock["base_main_sha"] == "dc665a1e93573949040900faa65b46af3a3ea6d9"
from datetime import datetime, timezone
when = datetime.strptime(lock["updated_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
assert when >= datetime(2026,10,1,19,11,18,tzinfo=timezone.utc), "R2 UPDATED_AT_STALE would fire"
print("LOCK_SEAMS_OK")
EOF
```
Expected: `LOCK_SEAMS_OK`. Failure: the named predicted refusal R1/R2 — fix the seam on L1's
terms (see above), never the court.

### 5. Commit the release tree, THEN run the court (order is load-bearing)

The court reads gitlinks from the git rev (`git ls-tree <subject>`, court line 243), not the
worktree. Running it pre-commit yields false `GITLINK_PIN` refusals against the old recorded
pins of any not-yet-committed state.

```bash
git add -A && git commit -m "release: v26.10.1 bump (lanes L1-L10)"   # coordinator
python3.11 scripts/lock_crown_court.py; echo "exit=$?"
```
Expected: `exit=0`, JSON `"standing": "ALIVE"`, `"violations": []`,
`"subject": "<release commit sha>"`.

Failure codes → owning seam:

| code | meaning | owner |
|---|---|---|
| LOCK_UNPARSEABLE | lock not valid TOML | L1 |
| PIN_SHAPE | a pin is not lowercase-40-hex | L1 |
| SUBMODULE_SET / SUBMODULE_DUPLICATE | lock paths != .gitmodules / duplicate path | structural; investigate |
| GITLINK_PIN | committed gitlink != lock `[submodules]` commit | coordinator crown step |
| SECTION_PIN | producer section sha != `[submodules]` commit | L1 |
| WORKFLOW_DEFAULT_MISSING / WORKFLOW_CONTAINER_TAG | sync workflow defaults missing / tag != `[container].tag` | L4 or L1 |
| PROJECTION_PARITY | workflow defaults != ontology.ttl defaults | L4 |
| MARKETPLACE_DEFAULT_UNRECORDED | `bf9eccb3…` not cited inside CHANGELOG `## [v26.10.1]` section text | L3 (+L4 value) |
| RELEASE_IDENTITY | `[container].tag` != `[ggen].release` | L1 (predicted risk R1) |
| RELEASE_UNRECORDED | no `## [<release>]` section in CHANGELOG | L3 |
| CONTAINER_STANDING | standing vocab / republish-without-BLOCKED+failure / bad digest | L1 (`requires_republish=true` needs `standing="BLOCKED"` + `failure` text — RESOLUTIONS pins exactly that) |
| BASE_NOT_ANCESTOR / BASE_IS_SUBJECT | base_main_sha ancestry | L1 (dc665a1e verified ancestor of HEAD at baseline) |
| UPDATED_AT_SHAPE / _STALE / _FUTURE | updated_at format or clock window | L1 (predicted risk R2; window >= 2026-10-01T19:11:18Z, <= commit time) |

### 6. Parse checks (TOML / YAML / TTL)

```bash
python3.11 -c "import tomllib; tomllib.load(open('ecosystem.lock.toml','rb')); print('TOML_OK')"
python3.11 -c "import yaml; yaml.safe_load(open('.github/workflows/ggen-ecosystem-sync.yml').read()); print('YAML_OK')"
python3.11 -c "from rdflib import Graph; Graph().parse('ontology.ttl', format='turtle'); print('ONTOLOGY_TTL_OK')"
python3.11 -c "from rdflib import Graph; Graph().parse('ecosystem.ttl', format='turtle'); print('ECOSYSTEM_TTL_OK')"
```
Expected: four OK lines (all four probes verified installed at baseline: yaml OK, rdflib OK).
Failure meaning: syntax broken by a lane edit; `TOML_OK` failing also implies the court's
LOCK_UNPARSEABLE, so fix before re-running the court. (`rapper` exists at
/opt/homebrew/bin/rapper as a second TTL opinion if rdflib and rapper ever disagree.)

### 7. Submodule status vs RESOLUTIONS targets (all 6, no +/-/U prefixes)

```bash
cat > /tmp/v26101-targets.txt <<'EOF'
71de04a60db723764fab5afe042b42937b471e0e vendor/autofde-lab
7bad16ab4c20d0eeb90adca1c90a6f3f4d5900dc vendor/beam4pm
ff96f04e8c7b851e5cca53f3faf5ce1d5f43ce6e vendor/ggen
bf9eccb3420134d4850dd49a5cbbef7dc35f20e2 vendor/ggen-marketplace
0abed8a35db68c18bba6982b266dd7546c162d1c vendor/ggen_igniter
a7352d818dbcaa15909833f13ac367dc5950a7a9 vendor/wasm4pm
EOF
diff <(git submodule status | awk '{sub(/^[+-U ]+/,"",$1); print $1, $2}' | sort -k2) \
     <(sort -k2 /tmp/v26101-targets.txt) && echo SUBMODULES_AT_TARGETS
```
Expected: `SUBMODULES_AT_TARGETS` (empty diff; no `+`/`-`/`U` prefixes on raw
`git submodule status`). Failure meaning: a vendor checkout or recorded pin deviates from
RESOLUTIONS.md — re-run step 3, then investigate; never re-point a pin to make the diff pass.

### 8. ggen.lock regen

```bash
which ggen        # baseline observed: /Users/sac/.local/bin/ggen (ggen 26.9.28)
ggen sync         # ggen.lock header: "generated by `ggen sync`. Do not edit."
git diff -- ggen.lock
```
Expected: `ggen sync` resolves the pipeline against `vendor/ggen-marketplace` at
`bf9eccb3…`; `ggen.lock` either unchanged or its `content_hash` values updated to the packs
at the new marketplace pin. Failure meaning: resolve/enrich/extract failure = lock and
marketplace pin incoherent — the lock regen must not be hand-patched (`Do not edit.`); fix
the pin or the pack source. Run AFTER step 3 (packs come from the materialized checkout).

### 9. No-stale-pins check (v26.9.25-era AND v26.9.29-era pins, outside historical surfaces)

```bash
grep -rnE 'v26\.9\.(22|25|29)|2c4c4c7e2a4eb33ebe2ad9ab23725af3c476a637|637b561cc6384fc9ac0e4282d048cc7624256258|38ccda683b499db16f4a6425a7d080ad0c86607c' \
  --include='*.toml' --include='*.yml' --include='*.yaml' --include='*.ttl' --include='*.cff' \
  --exclude-dir=vendor --exclude-dir=archive --exclude-dir=receipts --exclude-dir=fixtures \
  --exclude-dir=jira --exclude-dir=releases --exclude-dir=node_modules \
  . | grep -v '^./CHANGELOG.md:'
echo "stale_pin_grep_exit=$?"   # grep exit 1 (no matches) is the PASS
```
Expected: NO output, exit 1 (grep found nothing in machine-readable surfaces outside the
excluded historical surfaces: vendor, archive, receipts, tests/fixtures, docs/jira,
docs/releases, CHANGELOG historical sections).
Failure meaning: a projection seam still names a pre-v26.10.1 pin. Pre-bump ground truth
(L9 snapshot 19:30Z, expected to be gone after lanes land): lock `release`/`tag` v26.9.29 +
`base_main_sha` 38ccda68; README.md:13/:86 v26.9.25-era standing lines (L6);
docs/CURRENT-RELEASE-STANDING.md:10 `2c4c4c7e…` (L5); docs/TRANSPORT.md v26.9.25 narrative
(L7). Prose mentions of past crowns inside clearly-dated historical notes in current-facing
docs are tolerable; any MACHINE surface hit (toml/yml/ttl/cff) is a hard stop.

## Anti-vacuity note

The court is proven non-vacuous upstream (23/23 refusal mutants, per its docstring and
`tests/lock_contracts/test_lock_crown_court.py`); this checklist's steps 4/6/7/9 carry their
own expected outputs so a silently-green integration is distinguishable from a checked one.
If every step above passes, record the court JSON from step 5 as the v26.10.1 court receipt
and tag `v26.10.1` on that exact commit.
