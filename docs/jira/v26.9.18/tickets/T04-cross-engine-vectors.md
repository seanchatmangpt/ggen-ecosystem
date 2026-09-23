# T04 — cross-engine vectors (canonical binding oracle)

- Repo: `seanchatmangpt/ggen-marketplace` (worktree: `~/wt-v26918/mkt-04-vectors`)
- Branch: `gpack/mkt-04-vectors` (pre-created off `origin/main` = `800b8c6c5`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md`

## Goal

Appendix D `cross-engine/*`: RDF-term vectors + expected canonical bindings in
SPARQL Results JSON typed form (§23/§24) — the comparison oracle both engines
must agree on (Appendix E row 4).

## Scope (create)

```
packs/ggen-pack-spec-pack/vectors/
├── README.md                      # oracle law: §24 typed form is the comparison target;
│                                  # lexical accidents (quoted IRIs, bare ints) are NOT
├── rdf-iri/                       # ontology.ttl with an IRI-valued triple; query.rq;
│                                  # expected.json ({"type":"uri","value":...})
├── simple-literal/                # {"type":"literal","value":"..."} (no datatype)
├── datatype-literal/              # "42"^^xsd:integer → value "42" + datatype IRI (§24 example verbatim)
├── language-literal/              # "chat"@en → value + "xml:lang":"en"
├── unbound/                       # OPTIONAL miss → binding absent, not "" or null-string (§23)
└── order-by/                      # 5 rows, ORDER BY ?n; expected.json row order = the only
                                  # meaningful order; a sibling expected-unordered.json
                                  # (sorted multiset) documents §25 canonicalization
```

Each dir: `ontology.ttl` (tiny graph), `query.rq` (SELECT), `expected.json`
(SPARQL Results JSON: head.vars + results.bindings in §24 typed form).

## Acceptance (falsifiers)

1. Every expected.json is valid JSON with `head.vars` non-empty and bindings
   keyed exactly by head.vars (script-checked; command recorded).
2. `datatype-literal/expected.json` matches the §24 JSON example shape
   exactly (type/value/datatype keys).
3. order-by: expected.json row order ≠ lexicographic file order somewhere —
   i.e. ORDER BY is load-bearing, proven by a comment showing the two orders
   differ.
4. Each vector's query runs against ANY local SPARQL engine you can actually
   invoke in the worktree (record which engine + the real output diff vs
   expected.json canonicalized). If no engine is invokable, record BLOCKED
   with the exact missing tool — do not fabricate a comparison.

## Out of scope

Engine-side binding normalization (T14). Crown execution (wave 2).

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
