# T02 — spec-pack valid corpus (qualification/positive/)

- Repo: `seanchatmangpt/ggen-marketplace` (worktree: `~/wt-v26918/mkt-02-valid-corpus`)
- Branch: `gpack/mkt-02-valid-corpus` (pre-created off `origin/main` = `800b8c6c5`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md`

## Goal

Appendix D `valid/*` corpus as self-contained fixture packs under the spec
pack, each one exactly the §90 recommended shape.

## Scope (create)

```
packs/ggen-pack-spec-pack/qualification/positive/
├── README.md                        # what each fixture proves + how to run it
├── minimal-portable-pack/           # §91 VERBATIM: pack.toml, ontology.ttl,
│                                    # queries/message.rq, gates/010_required.rq,
│                                    # templates/hello.txt.tera, expected output
├── two-semantic-dependencies/       # consumer pack with TWO gp:requiresPack deps,
│                                    # each gp:dependencyScope exactly {SEMANTICS} (§26/§27);
│                                    # dependee packs are tiny inline fixture dirs beside it
├── portable-tera-fanout/            # one query with ORDER BY, for_each template
│                                    # rendering N deterministic targets (§25 order law)
└── consumer-alias/                  # §9: fixture showing [packs] alias "payments"
                                     # vs canonical "acme-payments-pack" and the receipt
                                     # fields that must preserve both
```

Each fixture pack: strict §7.1 pack.toml + ontology.ttl that self-describes
with `gp:profile gp:Portable1` + `gp:authorityCeiling gp:Construct`. The
`two-semantic-dependencies` dependees declare semantics only (no templates/)
which is lawful (§73) — the fixture README states engines without §73 support
report UNSUPPORTED rather than redefine Pack.

## Acceptance (falsifiers)

1. Every fixture's Turtle + TOML parses for real (commands recorded).
2. `minimal-portable-pack` is byte-faithful to §91 — diff against the RFC
   text and record it.
3. The `portable-tera-fanout` query uses ORDER BY and its expected target set
   is stated in README (order-invariance witness for wave-2 courts).
4. README states, per fixture, which Appendix E crown row it feeds.

## Out of scope

Running Rust ggen or Igniter against the fixtures (wave 2 / Appendix E).
gates/ ontology edits (T01). Negative fixtures (T03).

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:23:26Z | PARTIAL_ALIVE | gpack/mkt-02-valid-corpus@ebb0a78a6 (base 800b8c6c5) | fixtures + guards written; baseline captured pre-change: validate exit 0 (318 packs), pytest 3 failed/199 passed (pre-existing: book_nav, turtle_literals bounded<=950, comment-only set) | full-suite re-run + receipts |
| 2026-09-18T06:23:26Z | ALIVE | gpack/mkt-02-valid-corpus@ebb0a78a6 | `python3.11 scripts/marketplace.py validate` exit 0 (319 packs, semantic 43); catalog determinism `cmp` exit 0; `fingerprint` exit 0; `check_cross_pack_references.py` exit 0, skipped=1235 == baseline (0 contributed); RFC-91 byte-diff all 6 files exit 0; `python3.11 -m pytest tests/ scripts/ -q` exit 1 — 3 failed/215 passed, failure set name-identical to clean baseline (3 pre-existing, zero new; +16 = tests/test_gpack_valid_corpus.py all passing, incl. §79 sabotage twins + real rdflib query/gate execution) | none |
