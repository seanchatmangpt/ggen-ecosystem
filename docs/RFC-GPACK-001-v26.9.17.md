# RFC-GPACK-001 v26.9.17

## GGEN Semantic Pack Protocol

### Portable Semantic Manufacturing Units for `ggen`, `ggen_igniter`, Marketplaces, and Future Engines

**Status:** Proposed Standard
**Version:** v26.9.17
**Category:** Semantic Manufacturing / Package Composition / Conformance
**Intended audience:** implementers of `ggen`, `ggen_igniter`, ggen marketplaces, pack authors, semantic-runtime authors, generator-framework authors, conformance-court authors, supply-chain tooling, and systems consuming ontology-backed manufacturing units.

---

# Abstract

This specification defines the **GGEN Pack** as a portable, content-addressable, ontology-backed semantic manufacturing unit.

A GGEN Pack is not merely a directory of templates.

It is not merely an RDF file.

It is not merely a code generator.

It is not merely an archive distributed by a marketplace.

A conforming pack binds:

$$
\boxed{
Identity
+
Semantics
+
Dependencies
+
Admission
+
Projection
+
Authority
+
Evidence
+
Lifecycle
}
$$

into one independently identifiable unit whose behavior can be resolved, admitted, composed, manufactured, receipted, replayed, and qualified by more than one implementation.

The governing relation is:

$$
\boxed{
Artifact = \mu(O^*,P,C)
}
$$

where:

* \(O^*\) is admitted semantic observation;
* \(P\) is an admitted pack;
* \(C\) is an admitted consumer context;
* \(\mu\) is lawful deterministic manufacture.

A generated artifact acquires no authority merely because it was generated.

A pack acquires no authority merely because it was installed.

A dependency acquires no projection or actuation authority merely because its graph was imported.

A successful renderer return does not by itself establish a successful consequence.

A pack claim acquires standing only from bounded evidence over an exact subject.

This specification defines:

1. a stable pack identity;
2. a minimal bootstrap manifest;
3. semantic pack metadata represented in RDF;
4. explicit separation of queries from refusal gates;
5. explicit renderer profiles;
6. canonical SPARQL result semantics;
7. dependency and composition semantics;
8. content-addressed pack identity;
9. projection and target ownership;
10. authority ceilings;
11. deterministic manufacture requirements;
12. receipts and replay;
13. lifecycle and compatibility semantics;
14. marketplace behavior;
15. portable and implementation-specific profiles;
16. executable conformance courts and falsifiers.

The objective is:

$$
\boxed{
\frac{\partial Interpretation}
{\partial Implementer}
\rightarrow 0
}
$$

Two independent conforming engines should be able to consume the same portable pack and agree on its identity, admitted graph, queries, refusals, target ownership, and portable consequences without private coordination.

---

# 1. Normative Language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** are normative.

A normative requirement is not considered demonstrated solely because source code appears to implement it.

Every conformance claim is scoped to:

```text
specification revision
implementation identity
pack identity
consumer identity
configuration identity
runtime/toolchain identity where material
executed court
persisted evidence
```

Inspection is not execution.

$$
Inspection \neq Execution
$$

Implementation is not verification.

$$
Implemented \neq Verified
$$

Generation is not authority.

$$
Constructed \not\Rightarrow Authorized
$$

Successful return is not independent consequence verification.

$$
SelfReport \neq PostconditionObservation
$$

---

# 2. Design Objective

The protocol SHALL preserve a small invariant core while permitting a large lawful implementation and composition space.

The target is:

$$
\boxed{
SmallInvariantCore
\times
LargeCompositionSpace
\times
ExecutableFalsifiability
\times
IndependentImplementation
}
$$

The protocol therefore distinguishes:

```text
pack semantics
pack transport
pack distribution
pack rendering
pack execution
pack qualification
```

These are related surfaces but are not interchangeable.

---

# 3. Foundational Laws

## 3.1 Received Is Not Admitted

$$
Received(P) \not\Rightarrow Admitted(P)
$$

Downloading, cloning, unpacking, locating, or reading a pack MUST NOT by itself grant the pack semantic standing.

---

## 3.2 Pack Is Not Capability

$$
PackIdentity \neq CapabilityIdentity
$$

A pack MAY provide more than one capability.

Multiple packs MAY provide implementations of one capability.

A capability MUST NOT be inferred solely from a directory or package name.

---

## 3.3 Pack Is Not Semantic Authority

$$
ArtifactIdentity \neq SemanticAuthority
$$

A compatibility pack may retain an old package identity without retaining canonical semantic authority.

An umbrella pack may expose dependencies without becoming authoritative for their semantics.

---

## 3.4 Capability Is Not Authority

$$
Capability \not\Rightarrow Authority
$$

The ability to generate, propose, calculate, render, plan, or describe an operation does not grant authority to execute an external consequence.

---

## 3.5 Query Is Not Gate

$$
\boxed{
Query \neq Gate
}
$$

A query retrieves or constructs information.

A gate attempts to falsify admission.

Their directory placement, execution semantics, return interpretation, receipts, and failure consequences MUST remain distinct.

---

## 3.6 Projection Is Not Source

$$
GeneratedArtifact \neq CanonicalSemanticSource
$$

When a pack declares an RDF graph as semantic authority, generated files MUST be treated as projections unless another explicit authority relation is admitted.

---

## 3.7 Dependency Is Not Ambient Authority

$$
Dependency \not\Rightarrow Projection
$$

$$
Dependency \not\Rightarrow DO
$$

Importing a dependency's graph MUST NOT silently activate its projections, hooks, external commands, or consequential behavior.

---

## 3.8 Declaration Order Is Not Meaning

For any composition whose semantics do not explicitly declare order:

$$
Compose(P_1,P_2)
=
Compose(P_2,P_1)
$$

with respect to admitted graph identity and all order-independent consequences.

Implementation container ordering, TOML key order, directory enumeration order, hash-map iteration order, and filesystem order MUST NOT accidentally become protocol semantics.

---

# 4. Prior Implementation Baseline

This section is informative. It records implementation reality against which this specification was designed.

## 4.1 Rust `ggen`

Observed subject:

```text
repository: seanchatmangpt/ggen
revision: ad3a7e661ae876c48bb3813be0f96a30913acd6d
```

The current Rust implementation resolves packs from consumer `[packs]` entries.

Its native pack shape requires:

```text
pack.toml
ontology.ttl
templates/**/*.tmpl
optional gates/*.rq
```

Its `pack.toml` schema is fail-closed and admits only:

```toml
[pack]
name = "..."
version = "..."
description = "..."
```

Its current semantics include:

* path-based pack references;
* git-based references;
* optional git `subdir`;
* local `extra_ontologies`;
* pack content hashing;
* `ggen.lock`;
* sorted template discovery;
* Tera templates;
* template frontmatter;
* SPARQL-driven projection;
* `gates/*.rq` as refusal gates;
* filesystem manufacture;
* receipts.

Current Rust gate semantics are:

```text
SELECT returning ≥1 row => violation
ASK returning true      => violation
```

and refusal occurs before projection/write.

---

# 4.2 `ggen_igniter`

Observed subject:

```text
repository: seanchatmangpt/ggen_igniter
revision: 15305cea430d66ede71e6a711634e3b5fab3ae09
```

The current Igniter implementation recognizes approximately:

```text
priv/ggen/<pack>/
├── pack.toml
├── ontology.ttl
├── gates/*.rq
└── templates/*.{eex,tmpl}
```

but presently:

* `pack.toml` is optional and not consumed by `GgenIgniter.Pack`;
* `gates/*.rq` are discovered as named query sources;
* `.eex` and `.tmpl` are selected as templates;
* default rendering is EEx;
* a real WASM-hosted Tera renderer also exists and is currently selected by `.tera`;
* multiple SPARQL engines are supported;
* current engines can expose different RDF-term lexical representations;
* reconciliation tracks stale generated outputs;
* Igniter-specific AST mutation and upstream generator composition are supported.

---

# 4.3 `ggen-marketplace`

Observed subject:

```text
repository: seanchatmangpt/ggen-marketplace
revision observed: 800b8c6c5d05e91ff3b2d3bbd99c095acbe09359
```

The marketplace already treats packs as ontology-backed manufacturing or semantic bundles.

It distinguishes structural profiles including:

```text
projection
semantic
project
```

and semantic responsibility classes including concepts such as:

```text
KernelPack
CapabilityPack
ProfilePack
WorldPack
CompatibilityPack
EvidencePack
ReleaseControlPack
UmbrellaPack
```

It also independently validates pack structure and performs bounded real-ggen manufacture/replay qualification.

---

# 4.4 Current Divergences

The following are known implementation divergences and motivate this RFC.

### D1 — Gate/Query Conflation

Rust:

```text
gates/*.rq = refusal law
```

Current Igniter:

```text
gates/*.rq = rendering query inputs
```

This specification resolves the ambiguity permanently.

---

### D2 — Renderer Ambiguity

Rust:

```text
*.tmpl = Tera + ggen frontmatter
```

Current Igniter:

```text
*.tmpl = selected with EEx templates
*.tera = real Tera/WASM rendering
```

A filename extension MUST NOT remain the sole authority for ambiguous renderer semantics.

---

### D3 — Manifest Authority

Rust parses `pack.toml` strictly.

Igniter presently does not read it during normal pack resolution.

Marketplace treats it as required identity.

This RFC defines one bootstrap identity contract.

---

### D4 — Pack Dependencies

Current packs cannot portably declare pack-to-pack dependencies as a first-class pack contract.

Consumers currently perform composition.

This RFC defines explicit dependency semantics.

---

### D5 — Semantic Import

The marketplace consolidation court established that no general exercised cross-pack semantic-import mechanism currently provides the desired:

```text
KernelPack
   ↓ semantic import
ProfilePack
```

relationship.

This RFC defines that missing boundary without pretending it already exists.

---

### D6 — RDF Result Shape

Different query engines may expose the same RDF term using different implementation-specific lexical forms.

A portable pack MUST NOT rely on those accidental representations.

---

# 5. Terminology

## 5.1 Pack

A **Pack** is a versioned semantic manufacturing unit.

Formally:

$$
\boxed{
P =
(I,G,D,Q,A,\Pi,R,L)
}
$$

where:

* \(I\) — identity;
* \(G\) — semantic graph;
* \(D\) — dependency declaration;
* \(Q\) — query and rule surface;
* \(A\) — admission law;
* \(\Pi\) — projection/manufacturing surface;
* \(R\) — receipt/evidence contract;
* \(L\) — lifecycle metadata.

---

## 5.2 Consumer

A **Consumer** is the project or environment composing one or more packs.

---

## 5.3 Bootstrap Manifest

`pack.toml` is the minimal transport/bootstrap identity header.

It is not the general semantic metadata store.

---

## 5.4 Pack Graph

The **Pack Graph** is RDF carried by the pack that expresses domain semantics and MAY express pack-protocol metadata.

---

## 5.5 Query

A **Query** selects or derives information.

A query result MAY become a rendering binding.

It does not refuse merely because rows exist.

---

## 5.6 Gate

A **Gate** attempts to identify a violation.

A positive violation result refuses the transition under examination.

---

## 5.7 Projection

A **Projection** deterministically constructs an artifact from admitted graph state and admitted bindings.

---

## 5.8 Manufacture

**Manufacture** is the complete lawful transformation:

$$
AdmittedGraph
\rightarrow Bindings
\rightarrow Projection
\rightarrow Artifact
$$

within a bounded declared consequence surface.

---

## 5.9 Authority Ceiling

The **Authority Ceiling** is the highest class of consequence a pack is permitted to request or perform under the relevant profile.

---

## 5.10 Standing

**Standing** is a bounded conclusion supported by an exact evidence subject.

---

# 6. Canonical Pack Layout

A GGEN Pack MAY contain:

```text
<pack>/
├── pack.toml
├── ontology.ttl
│
├── ontology/
│   └── *.ttl
│
├── queries/
│   └── *.rq
│
├── gates/
│   └── *.rq
│
├── rules/
│   └── ...
│
├── templates/
│   └── ...
│
├── qualification/
│   ├── positive/
│   ├── negative/
│   └── ...
│
├── vectors/
│   └── ...
│
├── docs/
│   └── ...
│
└── provenance/
    └── ...
```

Only `pack.toml` and `ontology.ttl` are REQUIRED by `GGEN-PACK-CORE`.

Executable profiles impose additional requirements.

---

# 7. Bootstrap Manifest

## 7.1 Required Schema

The core bootstrap manifest SHALL remain deliberately small:

```toml
[pack]
name = "example-pack"
version = "1.2.3"
description = "Example semantic manufacturing pack."
```

`name`, `version`, and `description` are REQUIRED.

A Core v1 implementation MUST reject unknown keys inside `[pack]`.

---

## 7.2 Why the Manifest Remains Small

The manifest exists to answer:

```text
What object is this?
Which version does it claim?
What is it called?
What is its human summary?
```

It MUST NOT become a second ontology.

Dependencies, capabilities, pack classes, lifecycle relations, authority ceilings, qualification semantics, target ownership, and protocol extensions SHOULD live in RDF.

---

# 8. Bootstrap Identity and Semantic Identity

The bootstrap manifest and semantic graph MUST NOT become competing authorities.

Let:

$$
I_B = BootstrapIdentity
$$

$$
I_S = SemanticIdentity
$$

Admission requires:

$$
\boxed{
Project(I_S)=I_B
}
$$

where the semantic graph declares the corresponding identity.

A disagreement is:

```text
REFUSED:PACK_IDENTITY_MISMATCH
```

---

# 9. Consumer Alias vs Canonical Pack Name

Consumer configuration MAY assign a local alias.

Example:

```toml
[packs]
payments = { path = "../packs/acme-payments-pack" }
```

where:

```toml
[pack]
name = "acme-payments-pack"
```

The engine MUST preserve both:

```text
consumer_alias = payments
canonical_name = acme-payments-pack
```

The alias MUST NOT overwrite canonical pack identity in receipts or dependency resolution.

Strict marketplace publication MAY require:

```text
directory_name == canonical_name
```

Local composition need not.

---

# 10. Semantic Pack Vocabulary

A pack SHOULD self-describe inside its admitted graph.

Informative example:

```turtle
@prefix gp: <https://ggen.dev/ns/pack#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<urn:ggen:pack:sa2a-pack>
    a gp:Pack ;
    gp:name "sa2a-pack" ;
    gp:version "26.9.17" ;
    gp:profile gp:Portable1 ;
    gp:authorityCeiling gp:Construct ;
    gp:providesCapability <urn:capability:sa2a> .
```

The canonical vocabulary SHOULD include at least:

```text
gp:Pack
gp:PackRequirement
gp:Capability
gp:Profile
gp:Renderer
gp:AuthorityCeiling
gp:TargetOwnership
gp:LifecycleState
gp:CompatibilityRelation
gp:QualificationProfile
```

---

# 11. Pack Classes

Pack classes describe semantic responsibility.

They MUST NOT implicitly grant execution rights.

Standard class concepts include:

```text
KernelPack
CapabilityPack
ProfilePack
WorldPack
CompatibilityPack
EvidencePack
ReleaseControlPack
UmbrellaPack
ProtocolPack
```

A class is descriptive semantic metadata.

$$
Class(P) \not\Rightarrow Authority(P)
$$

---

# 12. Profiles

This RFC defines several profiles.

## 12.1 `GGEN-PACK-CORE-1`

Requires:

```text
pack.toml
ontology.ttl
identity correspondence
content identity
path safety
```

No projection engine is required.

---

## 12.2 `GGEN-PACK-PORTABLE-1`

Adds:

```text
portable SPARQL query semantics
portable gate semantics
explicit renderer identity
canonical RDF binding representation
deterministic target projection
portable receipt envelope
```

This is the primary cross-engine interoperability profile.

---

## 12.3 `GGEN-PACK-RUST-1`

Describes capabilities specific to Rust `ggen`, including compatible native projection/write surfaces.

It MAY extend portable behavior.

It MUST NOT redefine Core terms.

---

## 12.4 `GGEN-PACK-IGNITER-1`

Describes Igniter-specific extensions including:

```text
EEx rendering
Igniter task composition
AST codemods
reconciliation
stale-file handling
```

It MUST NOT redefine Core terms.

---

## 12.5 `GGEN-PACK-MARKETPLACE-1`

Adds:

```text
distribution
snapshot identity
archive requirements
lifecycle publication
qualification metadata
catalog projection
```

---

# 13. Query Surface

Portable named queries SHALL live under:

```text
queries/*.rq
```

A portable projection MUST NOT depend on `gates/*.rq` as ordinary render bindings.

Queries SHOULD be processed in canonical lexical path order when execution order matters operationally.

However, independent SELECT queries MUST NOT become semantically order-dependent unless explicitly declared.

---

# 14. Gate Surface

Admission gates SHALL live under:

```text
gates/*.rq
```

A gate SHALL be interpreted as a falsifier.

For a SELECT gate:

$$
Violation =
RowCount > 0
$$

For an ASK gate:

$$
Violation =
true
$$

Therefore:

$$
\boxed{
GatePass = AttemptObserved \land ViolationAbsent
}
$$

A gate that never actually executed MUST NOT be reported as passed.

---

# 15. Gate Evidence

Every gate result SHOULD bind:

```text
gate identity
gate digest
subject graph identity
attempt observed
violation rows or ASK value
decision
typed refusal if applicable
```

A negative test is valid only when the attack reached the gate.

---

# 16. Gate Messages

A gate SHOULD contain or reference a stable machine-readable refusal identity.

Human prose MAY additionally be provided.

Example conceptual metadata:

```text
id: GPACK-ONTOLOGY-MISSING-NAME
message: Every gp:Pack requires exactly one gp:name.
```

The refusal identifier, not mutable prose, SHOULD be the stable automation key.

---

# 17. Renderer Profiles

Renderer identity MUST be explicit.

A conforming implementation MUST NOT infer ambiguous semantics solely from `.tmpl`.

Standard renderers initially include:

```text
gp:Tera1
gp:EEx1
```

Future renderers MAY be registered.

---

# 18. Tera Portable Renderer

`gp:Tera1` is the RECOMMENDED portable renderer.

Rust `ggen` already provides a native Tera implementation.

`ggen_igniter` already contains a real Tera implementation hosted through WASM.

A `GGEN-PACK-PORTABLE-1` implementation claiming Tera support MUST render the portable Tera corpus equivalently.

---

# 19. EEx Renderer

`gp:EEx1` is an Igniter extension.

A pack requiring EEx MUST advertise that requirement.

A Rust implementation lacking EEx MUST classify such a projection as:

```text
UNSUPPORTED:RENDERER:EEx1
```

rather than pretending the pack itself is malformed.

---

# 20. Filename Extensions

Recommended conventions:

```text
*.tera     → Tera
*.eex      → EEx
*.rq       → SPARQL
*.ttl      → Turtle
```

Legacy `.tmpl` MAY remain supported.

However:

```text
extension(".tmpl") != sufficient renderer identity
```

For new portable packs, `.tera` is RECOMMENDED for Tera templates.

---

# 21. Legacy `.tmpl`

Rust legacy `.tmpl` SHALL be interpreted according to the Rust legacy profile.

Existing Igniter `.tmpl` behavior MAY remain available under the Igniter legacy profile.

A new portable pack MUST NOT depend on this ambiguity.

---

# 22. Template Frontmatter

Portable Tera projections MAY use a normalized frontmatter contract.

Example:

```yaml
---
renderer: tera1
to: "lib/generated/{{ module_name }}.ex"
query: modules
for_each: modules
write: managed
---
```

The exact field schema SHALL be versioned.

Unknown normative fields MUST fail closed within a declared profile.

---

# 23. Canonical SPARQL Binding Model

Cross-engine portability requires a stable RDF-term model.

A binding MUST preserve RDF term identity.

A conforming canonical binding therefore distinguishes:

```text
IRI
blank node
simple literal
language literal
datatype literal
unbound
```

An implementation MUST NOT make portability depend on:

```text
"<https://example.org/x>"
```

versus:

```text
"https://example.org/x"
```

or:

```text
"42"^^<xsd:integer>
```

versus:

```text
42
```

as accidental engine output.

---

# 24. Canonical Binding Representation

The normative abstract representation is equivalent to SPARQL Query Results typed bindings.

Conceptually:

```json
{
  "type": "literal",
  "value": "42",
  "datatype": "http://www.w3.org/2001/XMLSchema#integer"
}
```

Renderers MAY expose convenience scalar views.

Portable conformance MUST use the canonical typed form as the comparison oracle.

---

# 25. Result Ordering

A query result has meaningful order only when the query establishes it.

A portable projection depending on row order MUST use `ORDER BY`.

Absent `ORDER BY`, consumers MUST treat row ordering as unspecified.

An engine MAY canonicalize unordered result sets for hashing and replay.

---

# 26. Pack Dependencies

Dependencies SHALL become pack-owned semantic declarations.

A dependency MUST declare which surfaces are required.

A dependency is not simply "load everything."

The initial dependency surface algebra is:

$$
Scope \subseteq
\{
SEMANTICS,
LAW,
PROJECTION
\}
$$

---

# 27. Semantic Dependency

A semantic dependency imports admitted graph semantics without activating projection.

Example conceptually:

```text
requires:
    pack = ggen-core-kernel
    scope = {SEMANTICS}
```

Therefore:

$$
ImportSemantics(Q)
\not\Rightarrow
RunProjection(Q)
$$

---

# 28. Law Dependency

A law dependency explicitly imports the selected admission constraints.

It MUST be intentional.

Law MUST NOT arrive accidentally through mere semantic vocabulary reuse.

---

# 29. Projection Dependency

A projection dependency allows another pack's projection surface to participate.

This is the strongest dependency surface and MUST be explicit.

---

# 30. Full Composition

A dependency may request:

$$
\{
SEMANTICS,
LAW,
PROJECTION
\}
$$

but `FULL` MUST be represented as the explicit union rather than assumed from ordinary dependency.

---

# 31. Capability Dependency

A pack MAY depend on a capability rather than one exact pack.

Example:

```text
requires capability:
    RDF_CANONICALIZATION
```

Resolution of a capability provider MUST be deterministic and receipted.

If multiple incompatible providers exist and no selection rule resolves them:

```text
REFUSED:AMBIGUOUS_CAPABILITY_PROVIDER
```

---

# 32. Version Requirements

Pack dependencies MAY declare version constraints.

A resolved dependency closure MUST record exact resolved versions and exact content identities.

Constraint:

```text
>=1.2 <2
```

is not a sufficient replay identity.

Receipt:

```text
1.7.3
sha256:...
```

is.

---

# 33. Immutable Resolution

Strict qualification SHOULD resolve remote dependencies to immutable identities.

A branch name alone is insufficient for exact replay.

Example:

```text
main
```

MAY be a discovery input.

The receipt MUST record the actual resolved commit and content digest.

---

# 34. Dependency Graph

The complete resolution result is:

$$
DAG(P)
$$

unless an explicitly supported cyclic semantic relation exists.

Projection dependency cycles MUST be refused unless a future profile explicitly defines their fixed-point semantics.

Default:

```text
REFUSED:DEPENDENCY_CYCLE
```

---

# 35. Composition Conflicts

Composition MUST detect at least:

```text
DUPLICATE_SEMANTIC_AUTHORITY
TARGET_OWNERSHIP_CONFLICT
DEPENDENCY_VERSION_CONFLICT
AUTHORITY_JOIN_INVALID
CAPABILITY_PROVIDER_AMBIGUOUS
PROJECTION_CYCLE
```

Conflicts MUST fail closed unless an explicit resolution relation exists.

---

# 36. One Failed Edge Is Topology

A failed dependency edge does not prove every possible composition invalid.

Resolvers SHOULD report the narrowest failed edge.

$$
FailedEdge \neq FailedGraphUniverse
$$

---

# 37. Content Identity

Every admitted pack MUST have a canonical source digest.

The required interoperable algorithm for Core v1 is SHA-256.

Implementations MAY additionally compute BLAKE3 or other hashes.

---

# 38. Canonical Pack Digest

Let every regular admitted source file have:

```text
normalized_relative_path
raw_bytes
```

Symlinks are forbidden in canonical pack source.

Files are sorted by UTF-8 path bytes.

Define:

$$
PackDigest =
SHA256(
"ggen-pack-v1\0"
\Vert
E_1
\Vert
E_2
...
\Vert
E_n
)
$$

where:

$$
E_i =
u64be(|path_i|)
\Vert path_i
\Vert u64be(|bytes_i|)
\Vert bytes_i
$$

Filesystem timestamps, UID, GID, mode bits beyond admission-relevant executable policy, and archive metadata MUST NOT affect semantic source identity.

---

# 39. Digest Scope

The canonical digest MUST include every source artifact capable of changing pack semantics or manufactured consequences.

That includes, where present:

```text
pack.toml
RDF sources
queries
gates
rules
templates
hook declarations
pack-owned qualification contracts
```

Runtime caches and emitted consequences MUST NOT be part of the source digest.

---

# 40. Distribution Archive

Archive bytes and PackDigest are separate concepts.

$$
ArchiveDigest \neq PackDigest
$$

A deterministic archive SHOULD be provided by marketplaces.

The semantic PackDigest remains independent of tar/gzip implementation details.

---

# 41. Consumer Input Closure

Manufacture identity MUST bind all inputs capable of changing consequences.

Conceptually:

$$
InputClosure =
PackClosure
\cup ConsumerGraph
\cup ExplicitConfig
\cup RendererIdentity
\cup QueryEngineIdentity
\cup AdmittedExtensions
$$

A receipt MUST identify enough of this closure to replay the claim it makes.

---

# 42. Target Ownership

Every projection SHOULD expose its target ownership domain before write.

Examples:

```text
exact path
path prefix
path template
managed marker region
```

Two projections claiming an incompatible target MUST NOT race.

---

# 43. Collision Law

If two independent projections resolve to the same target and no explicit merge contract exists:

```text
REFUSED:TARGET_OWNERSHIP_CONFLICT
```

The fact that both happened to render identical bytes MUST NOT silently legitimize duplicated ownership.

---

# 44. Projection Identity

Every projection SHOULD be identifiable independently of the file it emits.

Recommended identity tuple:

$$
ProjectionID =
(
PackID,
ProjectionName,
ProjectionDigest
)
$$

---

# 45. Generated/Manual Boundary

A pack MUST NOT silently overwrite manual content outside its admitted write contract.

Marker-based injection, managed-file replacement, checksum freezing, and structured AST mutation are distinct write profiles.

The profile MUST identify which applies.

---

# 46. Manufacture Authority

Filesystem construction inside an admitted consumer root is a bounded manufacture consequence.

It is not equivalent to arbitrary external system actuation.

Portable pack execution SHALL distinguish:

```text
CONSTRUCT_FILES
MUTATE_STRUCTURED_SOURCE
EXECUTE_PROCESS
NETWORK_DO
EXTERNAL_SYSTEM_DO
```

---

# 47. Default Authority Ceiling

Unless explicitly elevated by a higher-level authority system:

$$
\boxed{
PackAuthority \le CONSTRUCT
}
$$

A pack definition itself does not grant external `DO`.

---

# 48. Hooks

A hook MAY manufacture an intent.

$$
Hook \rightarrow Intent
$$

but:

$$
Intent \not\Rightarrow Authority
$$

A hook MUST NOT gain ambient external actuation authority merely by being present in a pack.

---

# 49. External Commands

A portable pack MUST NOT execute arbitrary external commands on the Core path.

Profiles that permit commands MUST:

1. declare the capability;
2. declare the authority boundary;
3. declare required inputs;
4. declare consequence classes;
5. produce receipts;
6. expose refusal behavior.

---

# 50. Determinism

For unchanged admitted inputs:

$$
\boxed{
\mu(O^*,P,C)_1
=
\mu(O^*,P,C)_2
}
$$

for all consequences claimed deterministic by the profile.

A deterministic profile MUST provide a replay court.

---

# 51. Input-Order Invariance

Where ordering is not semantically declared:

```text
reverse dependency declaration
shuffle filesystem enumeration
shuffle hash insertion order
```

MUST NOT change the canonical result.

---

# 52. Source Immutability During Manufacture

Manufacturing a pack MUST NOT silently rewrite its canonical source.

Qualification SHOULD establish:

$$
PackSourceBefore = PackSourceAfter
$$

unless the specific operation is an explicit pack-authoring mutation rather than pack consumption.

---

# 53. Fixed-Point Replay

For managed generated consequences:

$$
Sync(S_0)=S_1
$$

and:

$$
Sync(S_1)=S_1
$$

SHOULD hold for deterministic profiles.

---

# 54. Receipt

Every consequential manufacture SHOULD produce a receipt.

A portable receipt binds at least:

```text
spec revision
engine identity
engine version
pack canonical identity
pack digest
dependency closure
consumer identity
graph identity
query/gate identities
renderer identity
target identities
consequence digests
refusals
replay relation
standing
```

---

# 55. Portable Receipt Envelope

Informative shape:

```json
{
  "schema": "https://ggen.dev/receipt/pack/v1",
  "spec": "RFC-GPACK-001-v26.9.17",

  "engine": {
    "name": "ggen",
    "version": "26.9.17"
  },

  "subject": {
    "pack": "sa2a-pack",
    "version": "26.9.17",
    "pack_digest": "sha256:..."
  },

  "dependencies": [
    {
      "name": "example-kernel",
      "version": "1.4.2",
      "digest": "sha256:...",
      "scope": ["SEMANTICS"]
    }
  ],

  "graph": {
    "canonical_digest": "..."
  },

  "admission": {
    "gates_attempted": [],
    "refusals": []
  },

  "consequences": [
    {
      "target": "generated/example.ex",
      "operation": "MANAGED_WRITE",
      "sha256": "..."
    }
  ],

  "replay": {
    "status": "PASS"
  },

  "standing": "ALIVE"
}
```

---

# 56. Engine-Specific Receipts

Rust BLAKE3 receipt chains and Igniter reconciliation receipts MAY continue to exist.

They MAY be embedded or referenced by the portable envelope.

The portable envelope MUST NOT falsely imply those formats are byte-equivalent.

---

# 57. Receipt Is Not Standing by Name

A file called `receipt.json` is not evidence merely because it exists.

Standing depends on whether the relevant transition was actually observed.

---

# 58. Independent Consequence Verification

For claims beyond deterministic filesystem construction, the actor's own report SHOULD NOT be the sole evidence.

$$
ActuatorReport \neq IndependentObservation
$$

Profiles claiming external consequences MUST identify an independent postcondition boundary.

---

# 59. Reconciliation

An implementation MAY support reconciliation memory.

Igniter is expected to use this strongly.

Reconciliation MAY classify:

```text
new
unchanged
changed
stale
orphaned
conflicting
```

A stale generated target MUST be handled by an explicit policy.

---

# 60. Stale Policy

Standard policies MAY include:

```text
REFUSE
PRUNE
PRESERVE
```

The selected policy MUST be receipted.

A missing policy MUST NOT silently become destructive deletion.

---

# 61. Lifecycle

Pack lifecycle is distinct from versioning.

Standard lifecycle concepts include:

```text
Candidate
Active
Deprecated
CompatibilityOnly
Retired
Revoked
```

---

# 62. Deprecation

A deprecated pack SHOULD identify:

```text
successor capability
successor pack(s)
compatibility seam
migration rule
last version receiving new features
```

---

# 63. Compatibility Pack

A compatibility pack MAY preserve historical behavior that would otherwise appear undesirable.

That preservation is intentional contract, not authority to become the new canonical semantic model.

---

# 64. Marketplace

A marketplace is formally:

$$
\boxed{
M =
(PackSet,
AdmissionLaw,
ResolutionLaw,
SnapshotIdentity,
Standing)
}
$$

A marketplace is not merely a website or directory.

---

# 65. Marketplace Snapshot

A marketplace snapshot SHOULD bind:

```text
marketplace identity
marketplace version
source revision
pack set
pack digests
dependency graph digest
qualification profile
qualification receipt
```

---

# 66. Catalog

A catalog SHOULD be a deterministic projection from admitted pack state.

It SHOULD NOT become a second manually maintained source of pack truth.

---

# 67. Marketplace Admission

Marketplace admission MAY be stricter than Core pack admission.

Examples:

```text
directory name == canonical name
required documentation
required license metadata
qualification corpus
pack class
supply-chain provenance
```

Stricter admission MUST NOT redefine Core pack identity semantics.

---

# 68. Supply-Chain Provenance

Marketplaces SHOULD support established provenance standards rather than inventing incompatible equivalents.

Appropriate external standards MAY include:

```text
in-toto
SLSA provenance
SPDX
CycloneDX
Sigstore/DSSE
```

Their use is optional unless selected by a marketplace profile.

---

# 69. Remote Retrieval

Remote retrieval and semantic admission are separate.

$$
Fetched \neq Verified
$$

A transport lacking an authenticated expected digest MUST NOT be described as content-verified.

---

# 70. Read-Only Resolution

A read-only operation MUST NOT silently perform:

```text
network clone
cache deletion
cache mutation
pack installation
external actuation
```

when those consequences were not admitted by the operation.

Rust `resolve_read_only` is a valid existing example of this distinction.

---

# 71. Path Safety

A conforming implementation MUST prevent pack-controlled paths from escaping admitted roots.

At minimum, it MUST address:

```text
absolute-path escape
.. traversal
symlink escape
archive traversal
target traversal
```

---

# 72. Symlinks

The strict portable source profile refuses symlinks inside pack source.

A future profile MAY define safe symlink semantics.

Until then:

```text
REFUSED:PACK_SYMLINK
```

---

# 73. Semantic-Only Packs

A Core or semantic-profile pack MAY contain no projections.

Therefore:

$$
Pack \not\Rightarrow Template
$$

Engines whose current implementation requires at least one template MAY report semantic-only execution as unsupported until they implement that profile.

They MUST NOT redefine the abstract Pack to require projection.

---

# 74. Project Packs

A project pack MAY contain its own project-level configuration.

This is a profile, not the definition of Pack.

---

# 75. Umbrella Packs

An umbrella pack provides composition/default selection.

It MUST NOT duplicate canonical semantics merely to bundle them.

---

# 76. Public Capabilities

The public capability graph SHOULD be distinct from physical pack inventory.

$$
PackDirectory \neq PublicCapability
$$

A marketplace with 1,000 pack artifacts may expose far fewer canonical capability identities.

---

# 77. Conformance Philosophy

Conformance is earned by attempted falsification.

The central relation is:

$$
\boxed{
PASS =
AttemptObserved
\land
ForbiddenOutcomeAbsent
\land
RequiredOutcomeObserved
}
$$

where applicable.

---

# 78. Required Portable Courts

`GGEN-PACK-PORTABLE-1` SHOULD include at least:

```text
Court 1  — exact identity
Court 2  — manifest/graph correspondence
Court 3  — canonical pack digest
Court 4  — graph admission
Court 5  — Query ≠ Gate
Court 6  — gate sabotage
Court 7  — canonical binding equivalence
Court 8  — renderer equivalence
Court 9  — target ownership
Court 10 — declaration-order invariance
Court 11 — deterministic replay
Court 12 — source immutability
Court 13 — dependency closure
Court 14 — capability ambiguity refusal
Court 15 — fresh consumer
```

---

# 79. Gate Sabotage Court

For every normative admission gate, qualification MUST include a negative witness capable of causing the gate to fire.

Deleting or disabling the guard SHOULD cause the falsifier to survive.

A falsifier that passes regardless of whether the guard exists is presumed vacuous.

---

# 80. Cross-Engine Portable Court

A pack claiming portable standing MUST be consumable by at least two independent conforming implementations.

For Rust `ggen` and `ggen_igniter`, the court SHOULD compare:

```text
PackDigest
admitted graph identity
gate verdicts
query binding canonical form
target set
portable rendered bytes
replay result
```

---

# 81. Fresh Consumer Court

A qualifying consumer MUST be reconstructible from declared state.

Hidden producer-machine state MUST NOT be required unless explicitly part of the profile and receipt.

---

# 82. Standing Vocabulary

Recommended status vocabulary:

```text
UNKNOWN
PARTIAL_ALIVE
ALIVE
BLOCKED
BUILD_BROKEN
UNSUPPORTED
REFUSED:<TYPE>
```

These states MUST NOT be collapsed.

---

# 83. Unsupported vs Refused

`UNSUPPORTED` means the implementation lacks a requested capability.

`REFUSED` means the implementation possesses the boundary and deliberately rejected the subject.

$$
UNSUPPORTED \neq REFUSED
$$

---

# 84. Pack Conformance Is Not Consumer Runtime Correctness

A pack may be fully conforming while a particular generated application fails its own runtime tests.

Therefore:

$$
PackConformance
\not\Rightarrow
ConsumerRuntimeCorrectness
$$

Consumer qualification remains a separate court.

---

# 85. Implementation Migration — Rust `ggen`

Rust `ggen` SHOULD evolve toward this RFC through the smallest coherent changes.

### Required compatibility-preserving steps

1. preserve current `pack.toml`;
2. preserve `.tmpl` legacy profile;
3. preserve current gate semantics;
4. add explicit `queries/`;
5. support semantic-only Core packs;
6. support explicit renderer metadata;
7. add `.tera` portable discovery;
8. calculate portable SHA-256 PackDigest in addition to existing BLAKE3;
9. distinguish canonical pack name from consumer alias;
10. add semantic dependency resolution;
11. expose dependency scope;
12. emit portable receipt envelope;
13. add cross-engine conformance vectors.

Existing packs MUST NOT silently change semantics merely because the RFC implementation lands.

---

# 86. Implementation Migration — `ggen_igniter`

Igniter SHOULD evolve through:

1. require/read `pack.toml` for new Core profiles;
2. retain legacy optional-manifest behavior behind a compatibility profile;
3. stop using `gates/*.rq` as ordinary rendering queries in new packs;
4. discover `queries/*.rq`;
5. interpret `gates/*.rq` using refusal semantics;
6. retain old gate-as-query behavior only under legacy profile;
7. make renderer identity explicit;
8. route portable Tera through its existing real Tera engine;
9. avoid treating `.tmpl` as ambiguous under portable profiles;
10. recursively discover portable templates;
11. normalize RDF terms into canonical bindings;
12. implement dependency scopes;
13. calculate portable PackDigest;
14. emit portable receipt envelope;
15. retain reconciliation as an Igniter extension.

---

# 87. Implementation Migration — Marketplace

`ggen-marketplace` SHOULD progressively replace hard-coded side tables with admitted pack-owned semantics.

Candidates include:

```text
pack class
capabilities
dependencies
successors
authority ceiling
qualification profile
target ownership
lifecycle state
```

The marketplace SHOULD project these values into its catalog rather than owning a second authoritative representation.

---

# 88. Legacy Rust Profile

Existing Rust packs are not invalidated.

They are classified approximately as:

```text
GGEN-PACK-RUST-LEGACY-1
```

with:

```text
pack.toml strict
ontology.ttl
templates/**/*.tmpl = Tera/frontmatter
gates/*.rq = refusal law
```

---

# 89. Legacy Igniter Profile

Existing Igniter packs are not invalidated.

They are classified approximately as:

```text
GGEN-PACK-IGNITER-LEGACY-1
```

where:

```text
pack.toml optional
ontology.ttl
gates/*.rq = named rendering queries
templates/*.eex|*.tmpl = EEx-oriented discovery
```

No new pack SHOULD choose this profile unless preserving compatibility.

---

# 90. Portable Profile Migration

The recommended new-pack shape is:

```text
example-pack/
├── pack.toml
├── ontology.ttl
├── queries/
│   ├── modules.rq
│   └── fields.rq
├── gates/
│   └── 010_required.rq
├── templates/
│   └── module.ex.tera
└── qualification/
    ├── positive.ttl
    └── negative-missing-name.ttl
```

This structure gives each semantic role one unambiguous location.

---

# 91. Minimal Portable Example

`pack.toml`:

```toml
[pack]
name = "hello-pack"
version = "1.0.0"
description = "Portable hello-world semantic projection."
```

`ontology.ttl`:

```turtle
@prefix gp: <https://ggen.dev/ns/pack#> .
@prefix ex: <https://example.org/hello#> .

<urn:ggen:pack:hello-pack>
    a gp:Pack ;
    gp:name "hello-pack" ;
    gp:version "1.0.0" ;
    gp:profile gp:Portable1 ;
    gp:renderer gp:Tera1 ;
    gp:authorityCeiling gp:Construct .

ex:Hello
    ex:message "Hello from admitted RDF." .
```

`queries/message.rq`:

```sparql
PREFIX ex: <https://example.org/hello#>

SELECT ?message
WHERE {
  ex:Hello ex:message ?message .
}
```

`gates/010_required.rq`:

```sparql
PREFIX ex: <https://example.org/hello#>

SELECT ?subject
WHERE {
  BIND(ex:Hello AS ?subject)
  FILTER NOT EXISTS {
    ex:Hello ex:message ?message .
  }
}
```

`templates/hello.txt.tera`:

```text
{{ message }}
```

Expected consequence:

```text
Hello from admitted RDF.
```

---

# 92. SA2A Pack Example

The Semantic A2A specification can itself be represented as a pack:

```text
sa2a-pack/
├── pack.toml
├── ontology.ttl
├── rfc/
│   ├── RFC-SA2A-001.md
│   └── RFC-SA2A-002.md
├── queries/
├── gates/
├── templates/
├── corpus/
├── vectors/
├── qualification/
└── evidence/
```

The RFC documents are components of the pack.

They are not the entirety of the pack.

$$
RFC \subset Pack
$$

---

# 93. Self-Hosting

A mature GGEN ecosystem SHOULD manufacture its own pack scaffolds from this specification.

Desired closure:

$$
RFC
\rightarrow Ontology
\rightarrow Generator
\rightarrow Pack
\rightarrow Court
\rightarrow Receipt
$$

The hand-authored residue should approach the irreducible protocol seed.

---

# 94. Specification Pack

This RFC SHOULD eventually ship as:

```text
ggen-pack-spec-pack
```

containing:

```text
RFC source
pack vocabulary
SHACL/ShEx where useful
SPARQL gates
valid corpus
invalid corpus
cross-engine vectors
receipt schema
reference pack fixtures
migration fixtures
```

---

# 95. No Golden Trace Requirement

A conformance court MUST NOT require one exact internal execution trace when several lawful implementations exist.

It SHOULD specify invariants and externally observable relations.

For example:

```text
same admitted graph
same gate decision
same portable bindings
same target bytes
```

does not require identical internal function calls.

---

# 96. Exact Falsifier Requirement

Every important normative requirement SHOULD define an observation capable of disproving it.

Examples:

| Requirement         | Falsifier                                                              |
| ------------------- | ---------------------------------------------------------------------- |
| Gate != Query       | Put a returning SELECT in `queries/`; rows must not refuse             |
| Gate semantics      | Put same violating SELECT in `gates/`; sync must refuse                |
| Order invariance    | Reverse pack declaration order                                         |
| Digest completeness | Modify a gate; PackDigest must change                                  |
| Path safety         | Target `../../outside`                                                 |
| Target ownership    | Two packs claim same target                                            |
| Dependency scope    | SEMANTICS-only dependency contains projection; projection must not run |
| Renderer identity   | Feed EEx template to Tera-only profile                                 |
| Replay              | Execute unchanged manufacture twice                                    |
| Source immutability | Compare pack source before/after                                       |
| Fresh consumer      | Reconstruct in clean state                                             |

---

# 97. Evolution Rule

When a real defect is discovered:

$$
\boxed{
Defect
\rightarrow
MinimalCounterexample
\rightarrow
Falsifier
\rightarrow
PermanentCorpus
\rightarrow
CourtRevision
}
$$

A defect SHOULD reduce the intelligence required to detect that same failure in the future.

---

# 98. Protocol Stability

The protocol SHOULD evolve by additive profile extension where possible.

Core semantic terms SHOULD change only when a concrete falsifier demonstrates that the existing definition is insufficient or contradictory.

---

# 99. Extension Registration

Future implementations MAY introduce new:

```text
renderers
rule engines
write modes
receipt extensions
pack classes
qualification profiles
dependency surfaces
```

without modifying the Core protocol when those extensions preserve Core invariants.

---

# 100. Unknown Extension Behavior

If a pack requires an extension the implementation does not support:

```text
UNSUPPORTED:<extension>
```

is preferred over silent fallback.

---

# 101. Non-Goals

This specification does not require:

```text
one programming language
one RDF library
one SPARQL implementation
one renderer
one marketplace
one archive format
one cloud provider
one database
one planner
one workflow engine
one process-mining engine
one authority broker
one consumer framework
```

It standardizes the boundaries necessary for those systems to compose lawfully.

---

# 102. Architectural Compression

The complete protocol can be summarized as:

$$
\boxed{
Resolve
\rightarrow Admit
\rightarrow Compose
\rightarrow Select
\rightarrow Construct
\rightarrow Receipt
\rightarrow Replay
\rightarrow Standing
}
$$

with:

$$
Received \neq Admitted
$$

$$
Query \neq Gate
$$

$$
Capability \neq Authority
$$

$$
Dependency \neq AmbientProjection
$$

$$
Generated \neq Canonical
$$

$$
Execution \neq Verification
$$

$$
ReceiptName \neq Standing
$$

---

# 103. Thin Waist

The intended durable thin waist is:

$$
\boxed{
Identity
+
Graph
+
Dependency
+
Admission
+
Projection
+
Authority
+
Receipt
+
Lifecycle
}
$$

Rust, BEAM, WASM, Tera, EEx, Igniter, Ash, marketplaces, future renderers, future semantic stores, and future runtimes sit above or below that waist.

They are not the waist itself.

---

# 104. Success Criterion

This RFC succeeds when two independently implemented engines can receive an unfamiliar portable pack and, without private coordination:

1. identify the same pack;
2. compute the same portable digest;
3. admit the same graph;
4. resolve the same dependency closure;
5. refuse the same invalid subjects;
6. expose the same canonical bindings;
7. manufacture the same portable targets;
8. preserve the same target-ownership boundaries;
9. replay deterministically;
10. exchange mutually intelligible receipts.

Formally:

$$
\boxed{
Implementation_A(P,C)
\equiv
Implementation_B(P,C)
}
$$

for every behavior claimed by the portable profile.

---

# 105. Final Law

A GGEN Pack is a **semantic manufacturing unit with bounded authority and replayable evidence**.

Nothing received has standing merely because it was received.

Nothing queried is a violation merely because it returned information.

Nothing generated has authority merely because it was generated.

Nothing imported may silently widen another pack's consequence surface.

Nothing claiming determinism is deterministic until replay survives.

Nothing claiming portability is portable until an independent implementation agrees.

And every discovered defect should become permanent machine knowledge so that the same reasoning does not have to be purchased twice.

$$
\boxed{
Experience
\rightarrow Law
\rightarrow Falsifier
\rightarrow MachineKnowledge
}
$$

---

# Appendix A — Recommended Repository Mapping

```text
ggen
  → primary Rust reference implementation

ggen_igniter
  → primary BEAM/Igniter reference implementation

ggen-marketplace
  → reference registry / qualification implementation

ggen-pack-spec-pack
  → executable specification corpus
```

No one repository alone is the specification.

---

# Appendix B — Proposed Initial Namespace

```text
https://ggen.dev/ns/pack#
```

Illustrative terms:

```text
gp:Pack
gp:name
gp:version
gp:profile
gp:renderer
gp:providesCapability
gp:requiresCapability
gp:requiresPack
gp:dependencyScope
gp:importsSemantics
gp:importsLaw
gp:importsProjection
gp:authorityCeiling
gp:ownsTarget
gp:lifecycle
gp:successor
gp:qualificationProfile
gp:contentDigest
```

---

# Appendix C — Initial Typed Refusal Vocabulary

```text
REFUSED:PACK_MANIFEST_MISSING
REFUSED:PACK_MANIFEST_INVALID
REFUSED:PACK_IDENTITY_MISMATCH
REFUSED:PACK_GRAPH_MISSING
REFUSED:PACK_GRAPH_INVALID
REFUSED:PACK_SYMLINK
REFUSED:PACK_PATH_ESCAPE

REFUSED:QUERY_INVALID
REFUSED:GATE_INVALID
REFUSED:GATE_VIOLATION

REFUSED:DEPENDENCY_UNSATISFIED
REFUSED:DEPENDENCY_CYCLE
REFUSED:DEPENDENCY_VERSION_CONFLICT
REFUSED:AMBIGUOUS_CAPABILITY_PROVIDER

REFUSED:DUPLICATE_SEMANTIC_AUTHORITY
REFUSED:TARGET_OWNERSHIP_CONFLICT
REFUSED:AUTHORITY_JOIN_INVALID

REFUSED:RENDERER_AMBIGUOUS
REFUSED:RENDERER_PROFILE_MISMATCH
REFUSED:NONDETERMINISTIC_REPLAY
REFUSED:SOURCE_MUTATED_DURING_MANUFACTURE
REFUSED:RECEIPT_IDENTITY_MISMATCH
```

Implementation-specific codes MAY additionally exist.

---

# Appendix D — First Conformance Corpus

The first permanent corpus SHOULD contain at minimum:

```text
valid/minimal-portable-pack
valid/two-semantic-dependencies
valid/portable-tera-fanout
valid/consumer-alias

invalid/manifest-unknown-key
invalid/manifest-semantic-identity-mismatch
invalid/missing-ontology
invalid/gate-positive-select
invalid/path-traversal
invalid/symlink
invalid/dependency-cycle
invalid/ambiguous-capability
invalid/target-collision
invalid/renderer-mismatch

invariance/reversed-pack-order
invariance/reversed-file-discovery-order
invariance/repeated-sync

cross-engine/rdf-iri
cross-engine/simple-literal
cross-engine/datatype-literal
cross-engine/language-literal
cross-engine/unbound
cross-engine/order-by
```

---

# Appendix E — Required First Cross-Engine Crown

The first meaningful interoperable crown SHOULD use one real pack and run:

```text
Rust ggen
      │
      ├── admit pack
      ├── run gates
      ├── run portable query
      ├── render Tera
      ├── materialize files
      └── emit receipt
      │
      ▼
canonical evidence comparison
      ▲
      │
ggen_igniter
      │
      ├── admit same pack
      ├── run same gates
      ├── run same portable query
      ├── render through real Tera implementation
      ├── materialize files
      └── emit receipt
```

The crown requires:

$$
PackDigest_R = PackDigest_I
$$

$$
GraphDigest_R = GraphDigest_I
$$

$$
GateVerdicts_R = GateVerdicts_I
$$

$$
CanonicalBindings_R = CanonicalBindings_I
$$

$$
TargetBytes_R = TargetBytes_I
$$

$$
Replay_R = Replay_I = PASS
$$

This is the minimum evidence required before the ecosystem claims a pack is operationally portable across both engines.

---

# Appendix F — DfCM Requirement

Before any protocol choice eliminates a lawful implementation strategy, the specification author SHOULD ask:

```text
Can this requirement be stated as an invariant instead of an implementation?
Can an existing standard carry this semantic?
Can the same safety property be preserved with a smaller core?
Does this selection unnecessarily eliminate future runtimes?
Is this really protocol law, or merely today's reference implementation?
```

The default evolution order is:

$$
\boxed{
REUSE
\rightarrow COMPOSE
\rightarrow EXTEND
\rightarrow INVENT
}
$$

The protocol SHALL prefer structural interoperability to local reinvention.

---

# End of RFC-GPACK-001 v26.9.17
