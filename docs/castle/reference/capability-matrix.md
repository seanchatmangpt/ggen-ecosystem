# Reference: CASTLE remaining capability matrix

**Semantic source:** `ontology/castle-projection.ttl`

**Standing rule:** every row below is a CANDIDATE projection with authority ceiling CONSTRUCT. The table describes where useful capability belongs; it does not transfer ownership or establish runtime standing.

| Repository | Projected capability | Disposition | Projection target | Runtime placement |
|---|---|---|---|---|
| `seanchatmangpt/ggen` | Legacy manufacture compatibility | REPLACE | ggen_igniter | Knowledge/manufacture source |
| `seanchatmangpt/unrdf` | RDF kernel compatibility | WRAP | graphlaw | Semantic kernel behind owner |
| `seanchatmangpt/ex4pm` | Process execution kernel | WRAP | beam4pm | Process kernel behind runtime owner |
| `seanchatmangpt/ash_ex4pm` | Ash process projection | WRAP | process-intelligence | Ash adapter |
| `seanchatmangpt/zcode-cli` | External worker provider | WRAP | xaas | Provider edge |
| `seanchatmangpt/chatgpt-cloud-elixir` | Model-provider bridge | WRAP | xaas | Provider edge |
| `seanchatmangpt/ash_atlassian` | Work-system adapter | WRAP | ash_a2a | External-system adapter |
| `seanchatmangpt/ash_surface` | Human board surface | WRAP | castle | Human surface |
| `seanchatmangpt/ash_expo` | Mobile surface | WRAP | ash_surface | Mobile surface |
| `seanchatmangpt/ash_planning_center` | Planning Center adapter | WRAP | ash_a2a | External-system adapter |
| `seanchatmangpt/zoela` | Domain application surface | WRAP | castle | Domain tenant |
| `seanchatmangpt/cargo-cicd` | Software consequence adapter | WRAP | castle | Protected consequence adapter |
| `seanchatmangpt/chatman-ecosystem` | Strategy/doctrine knowledge | KEEP_KNOWLEDGE_PLANE | castle | Knowledge plane only |
| `seanchatmangpt/engineering-standards` | Engineering constitution knowledge | KEEP_KNOWLEDGE_PLANE | ggen-ecosystem | Knowledge plane only |
| `seanchatmangpt/agile-protocol-specification` | Protocol specification knowledge | KEEP_KNOWLEDGE_PLANE | ash_a2a | Knowledge plane only |
| `seanchatmangpt/praxis` | Historical semantic source | ABSORB | graphlaw | Historical source only |
| `seanchatmangpt/mfw` | Payment effect-chain falsifier | CANDIDATE_WRAP | graphlaw | Evidence/falsifier edge |
| `seanchatmangpt/ostar` | Proof-driven manufacture research | CANDIDATE_ABSORB | ggen_igniter | Manufacture research source |
| `seanchatmangpt/mmdio` | Semantic document projection | CANDIDATE_WRAP | ash_surface | Powerless document projection |
| `seanchatmangpt/wasm4pm-compat` | Process-evidence compatibility | CANDIDATE_WRAP | wasm4pm | Structural compatibility boundary |
| `seanchatmangpt/dteam` | OCEL payment effect-chain checker | CANDIDATE_ABSORB | beam4pm | Process-evidence donor only |
| `seanchatmangpt/mcpp` | Payment effect + settlement conformance | CANDIDATE_ABSORB | ash_a2a | Conformance donor only |
| `seanchatmangpt/chatman-nano-stack` | Application constitutional-control-plane research | CANDIDATE_ABSORB | castle | Application research donor only |

## Query surfaces

`queries/castle-capability-projection.rq` is the positive projection.

`queries/castle-projection-violations.rq` is the non-sovereignty court.

`queries/castle-projection-uniqueness.rq` is the repository/capability uniqueness court.

## Crown invariant

```text
XaaS   = RUNTIME_EXISTENCE
CASTLE = CONSEQUENTIAL_ADMISSIBILITY
```

No row in this matrix changes either equation.


## Seven-day payment frontier

The 2026-09-23..2026-09-30 intake adds `semantic_bit`, `a2a-rs`, `autotel`, `yawl`, and `cre` as evidence-only donors in `ontology/frontier/payment-effect-chain.ttl`. Existing `mfw`, `dteam`, and `mcpp` projections were reclassified above to match their merged payment/effect-chain capabilities. None becomes a new runtime, authority, settlement, or payments crown.
