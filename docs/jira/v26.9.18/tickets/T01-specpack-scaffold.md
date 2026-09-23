# T01 — ggen-pack-spec-pack scaffold (ontology + manifest + core gates)

- Repo: `seanchatmangpt/ggen-marketplace` (worktree: `~/wt-v26918/mkt-01-specpack-scaffold`)
- Branch: `gpack/mkt-01-specpack-scaffold` (pre-created off `origin/main` = `800b8c6c5`)
- RFC: `/Users/sac/ggen-ecosystem/docs/RFC-GPACK-001-v26.9.17.md`

## Goal

Create `packs/ggen-pack-spec-pack/` — the RFC's own executable specification
pack (§94), self-governed by the law it defines (§93 self-hosting).

## Scope (create exactly these; other tickets own subdirs)

```
packs/ggen-pack-spec-pack/
├── pack.toml                  # strict §7.1 schema: [pack] name/version/description ONLY
├── ontology.ttl               # the gp: vocabulary — see below
├── README.md                  # what the pack is, how courts consume it
├── gates/
│   ├── 010_identity.rq        # every gp:Pack has exactly one gp:name + gp:version (§16: stable refusal id in a comment)
│   └── 020_manifest_graph_correspondence.rq   # graph gp:name must equal the pack.toml name this pack ships under (§8)
└── qualification/README.md    # corpus layout contract (positive/ negative/ are T02/T03; vectors/ is T04)
```

`ontology.ttl` MUST declare (Appendix B namespace `https://ggen.dev/ns/pack#`,
Turtle, following the illustrative §10 shape):

- Classes: `gp:Pack gp:PackRequirement gp:Capability gp:Profile gp:Renderer
  gp:AuthorityCeiling gp:TargetOwnership gp:LifecycleState
  gp:CompatibilityRelation gp:QualificationProfile gp:PackClass`
- Profiles: `gp:Core1 gp:Portable1 gp:Rust1 gp:Igniter1 gp:Marketplace1
  gp:RustLegacy1 gp:IgniterLegacy1` (§12, §88, §89) — all `a gp:Profile`
- Renderers: `gp:Tera1 gp:EEx1` (§17)
- Authority ceilings: `gp:Construct` (default, §47) and the §46 ladder
  individuals (`gp:ConstructFiles gp:MutateStructuredSource gp:ExecuteProcess
  gp:NetworkDo gp:ExternalSystemDo`) with `gp:Construct` ≤-ordered above
  CONSTRUCT semantics documented in comments
- Lifecycle: `gp:Candidate gp:Active gp:Deprecated gp:CompatibilityOnly
  gp:Retired gp:Revoked` (§61)
- Pack classes (§11): KernelPack..ProtocolPack as `gp:PackClass` individuals
- Properties (App. B): gp:name gp:version gp:profile gp:renderer
  gp:providesCapability gp:requiresCapability gp:requiresPack gp:dependencyScope
  gp:importsSemantics gp:importsLaw gp:importsProjection gp:authorityCeiling
  gp:ownsTarget gp:lifecycle gp:successor gp:qualificationProfile gp:contentDigest
- Typed refusal vocabulary (App. C) as `gp:RefusalCode` individuals
- The spec pack describes ITSELF: `<urn:ggen:pack:ggen-pack-spec-pack> a gp:Pack ;
  gp:name "ggen-pack-spec-pack" ; gp:version "0.1.0" ; gp:profile gp:Portable1 ;
  gp:authorityCeiling gp:Construct ; gp:lifecycle gp:Candidate .`

## Acceptance (falsifiers, real execution)

1. Both gates RUN against this pack's own graph: `010` passes (zero rows),
   `020` passes. Positive witness recorded.
2. Gate sabotage (§79): a negative witness proving each gate can FIRE —
   mutate a copy of the graph (drop gp:name / mismatch the name) and show the
   row appears. Record commands + exit codes in History.
3. `pack.toml` parses and contains ONLY the three §7.1 keys.
4. Turtle parses (`riot --validate` if available, else any real parser; record
   which). No fake parse claims.

## Out of scope

qualification/positive/*, qualification/negative/*, vectors/* (T02/T03/T04);
marketplace catalog changes (T05); any Rust/Igniter change.

## Integration notes

Marketplace admission may impose extra metadata on packs (its own courts) —
match the shape of an existing well-formed pack (read 1-2 examples under
`packs/` first) so admission courts don't refuse on format.

## History

| ts (UTC) | standing | branch+SHA | gates+exits | remaining |
|---|---|---|---|---|
| 2026-09-18T06:09:02Z | PARTIAL_ALIVE | gpack/mkt-01-specpack-scaffold@800b8c6c5 | scaffold created: pack.toml (strict §7.1), ontology.ttl (gp: vocab + self-description), gates/010+020, README, qualification/README; no gates executed yet | acceptance 1-4 (gate runs, sabotage, toml, turtle), repo validation, commit |
| 2026-09-18T06:12Z | PARTIAL_ALIVE | gpack/mkt-01-specpack-scaffold@800b8c6c5 (uncommitted) | Acceptance 1 POSITIVE: rdflib 7.1.4 ran both gates on packs/ggen-pack-spec-pack/ontology.ttl (227 triples): 010 rows=0 exit 0; 020 rows=0 exit 0. Acceptance 2 SABOTAGE (§79, /tmp copies of graph): A drop gp:name → 010 rows=1 `GPACK-ONTOLOGY-MISSING-NAME` exit 1; B add 2nd gp:name → rows=1 `GPACK-ONTOLOGY-AMBIGUOUS-NAME` exit 1; C rename graph name → 020 rows=1 `REFUSED:PACK_IDENTITY_MISMATCH` exit 1; D drop gp:version → rows=1 `GPACK-ONTOLOGY-MISSING-VERSION` exit 1; E add 2nd gp:version → rows=1 `GPACK-ONTOLOGY-AMBIGUOUS-VERSION` exit 1; guard-deletion control: 010 minus MISSING-NAME branch vs sabotage-A → rows=0 exit 0 (guard load-bearing, witness non-vacuous). Acceptance 3: python3.11 tomllib strict-key assert → exit 0 (top-level={'pack'}, [pack]={name,version,description}). Acceptance 4: rdflib parse 227 triples exit 0 + rapper (raptor) 227 triples exit 0. | repo validation, commit |
| 2026-09-18T06:14Z | ALIVE | gpack/mkt-01-specpack-scaffold@0ff368db9 | committed 6 files (+591): `git commit` exit 0. Repo validation for changed scope: `python3.11 scripts/marketplace.py validate` exit 0 (packs 318→319, ontologies 472→473, native_gates 1505→1507, semantic profile 42→43, zero issues); catalog determinism `cmp` exit 0; fingerprint exit 0; `python3.11 -m pytest tests/ scripts/` → 199 passed, 3 failed — all 3 PRE-EXISTING at base 800b8c6c5 with byte-identical diagnostics when run without this pack (book-nav docs list; 1235 unparseable-statement bound; beam4pm entitlement list) — zero new failures. Post-commit gate re-run: 010 rows=0 exit 0, 020 rows=0 exit 0, validate exit 0. | none for T01. Edges recorded: gate 020 checks name correspondence only per ticket scope (version correspondence Project(I_S)=I_B on gp:version left to T02/T03 corpus courts); 3 pre-existing pytest failures at base SHA NOT fixed (outside ticket scope, fail identically without this pack); marketplace catalog registration is T05. |
