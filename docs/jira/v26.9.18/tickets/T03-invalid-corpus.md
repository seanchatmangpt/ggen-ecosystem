# T03 — spec-pack invalid corpus (qualification/negative/ + refusal assertions)

- Repo: `seanchatmangpt/ggen-marketplace` (worktree: `~/wt-v26918/mkt-03-invalid-corpus`)
- Branch: `gpack/mkt-03-invalid-corpus` (pre-created off `origin/main` = `800b8c6c5`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md`

## Goal

Appendix D `invalid/*` corpus: one fixture per typed refusal (Appendix C),
each with a machine-checkable assertion naming the expected refusal code.
§77 law: a negative test is valid only when the attack reaches the gate.

## Scope (create)

```
packs/ggen-pack-spec-pack/qualification/negative/
├── README.md                       # per fixture: attack, expected REFUSED:<CODE>, how to assert
├── manifest-unknown-key/           # §7.1 "MUST reject unknown keys" → REFUSED:PACK_MANIFEST_INVALID
├── manifest-semantic-identity-mismatch/  # §8 graph name ≠ manifest → REFUSED:PACK_IDENTITY_MISMATCH
├── missing-ontology/               # no ontology.ttl → REFUSED:PACK_GRAPH_MISSING
├── gate-positive-select/           # §14/§96: a returning SELECT placed in gates/ MUST refuse (rows>0)
├── query-positive-select/          # §96 row 1: SAME SELECT in queries/ MUST NOT refuse — the D1 falsifier pair
├── path-traversal/                 # template `to: ../../outside` → REFUSED:PACK_PATH_ESCAPE (§71)
├── symlink/                        # symlinked source file → REFUSED:PACK_SYMLINK (§72; store a setup.sh that creates it, NOT the symlink itself)
├── dependency-cycle/               # A requiresPack B, B requiresPack A → REFUSED:DEPENDENCY_CYCLE (§34)
├── ambiguous-capability/           # two providers, no selection rule → REFUSED:AMBIGUOUS_CAPABILITY_PROVIDER (§31)
├── target-collision/               # two packs, same target, no merge contract → REFUSED:TARGET_OWNERSHIP_CONFLICT (§43)
└── renderer-mismatch/              # EEx template into Tera-only profile → REFUSED:RENDERER_PROFILE_MISMATCH / UNSUPPORTED:RENDERER:EEx1 (§19)
```

Each fixture is a minimal but complete pack (pack.toml + ontology.ttl as
needed for the attack to REACH the law being tested). Add
`assert/refusal-code.txt` (exact expected code) + `assert/run.sh` that takes
an engine command template and exits 0 iff the engine's refusal output
contains the expected code — engines print refusals on stderr; run.sh greps
for BOTH the code and does not accept bare crash text as the refusal.

## Acceptance (falsifiers)

1. Every run.sh is itself executable against a "null engine" (a stub that
   echoes nothing) and FAILS — proving the assertion cannot pass vacuously.
   Record: `assert/run.sh <null-stub>` exit ≠ 0 for all 11.
2. The gate-positive-select / query-positive-select pair is present and
   cross-referenced in README (the D1 falsifier pair, §96 rows 1-2).
3. No fixture contains a real symlink in git (setup scripts only).

## Out of scope

Executing real engines (wave 2). T01/T02/T04 paths.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:12:50Z | PARTIAL_ALIVE | gpack/mkt-03-invalid-corpus@800b8c6c5 (clean, no prior-agent leftovers; retry start) | orient: ticket+RFC §6/7/8/13/14/19/26-34/42-43/71/72/77/96/AppB/AppC/AppD read; `git status` clean; baseline `python3.11 scripts/marketplace.py validate` exit 0 (318 packs) | build 11 negative fixtures + README + null-engine falsifier + repo tripwire test; NOTE: `packs/ggen-pack-spec-pack/pack.toml` root owned by T01 (out of scope) — validate will emit T01-owned MANIFEST_MISSING/ONTOLOGY_SOURCE_MISSING until T01 merges; evidence plan: validate with uncommitted stand-in T01 root |
| 2026-09-18T06:47:00Z | PARTIAL_ALIVE | gpack/mkt-03-invalid-corpus (uncommitted) | corpus built: 11 fixtures, 64 files; syntax gates rdflib Turtle×14 + SPARQL×2 + tomllib TOML×16 all OK exit 0; `run-null-falsifier.sh` exit 0 = 11/11 correctly FAIL vs null engine (acceptance 1); bidirectional probes: typed-refusal pass, bare-crash reject, wrong-law reject, D1-conflation reject, renderer alternate accept, symlink scratch-copy materialization OK, `find -type l` = 0 (acceptance 3); D1 pair byte-identical after fix (acceptance 2); `pytest tests/test_gpack_negative_corpus.py` 7 passed exit 0; full suite with stand-in T01 root: 3 failed/206 passed = exactly the 3 pre-existing base failures (199→206 passed, +7) | commit + final head observation |
| 2026-09-18T06:55:00Z | ALIVE | gpack/mkt-03-invalid-corpus@79de0b330 (parent 800b8c6c5, base not moved; tree clean) | commit 79de0b330 (64 files, +1422): feat(ggen-pack-spec-pack) citing §6/7.1/8/14/19/31/34/43/71/72/77/83/96/100 + App C/D; head-observed: `run-null-falsifier.sh` exit 0 (11/11); `pytest tests/test_gpack_negative_corpus.py -q` 7 passed exit 0; `marketplace.py validate` exit 2 = ONLY `REFUSED:MANIFEST_MISSING:ggen-pack-spec-pack` + `REFUSED:ONTOLOGY_SOURCE_MISSING:ggen-pack-spec-pack`, both T01-owned (proven: same command with uncommitted stand-in T01 root → exit 0, packs=319, and full pytest → same 3 pre-existing base failures only) | none in scope. Not taken (recorded): root scaffold=T01; real-engine execution=wave 2; gp:ownsTarget duplication skipped (frontmatter `to:` minimal-sufficient, §42 SHOULD); positive-evidence channel + consumer-config wiring contracts documented in README for wave 2. Operator did not have to write: all 64 files + falsifiers + tripwire test |
