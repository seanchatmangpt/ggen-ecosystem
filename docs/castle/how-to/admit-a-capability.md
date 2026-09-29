# How-to: admit a projected CASTLE capability

Use this procedure when a repository contains a useful capability but should not become a new irreducible CASTLE owner.

## 1. Observe an exact subject

Resolve the source repository to an exact branch and 40-character Git SHA.

Do not use a version label or repository name alone as evidence.

## 2. Decide whether the capability is genuinely distinct

Write one sentence describing the capability.

Then ask whether an existing CASTLE owner already owns that responsibility.

If the sentence duplicates an existing owner, project the source as a wrapper, donor, compatibility boundary, or replacement source instead of creating new ownership.

## 3. Choose a disposition

Use one of the bounded projection dispositions:

- `REPLACE` — preserve useful compatibility while moving permanent responsibility elsewhere.
- `WRAP` — expose the source only through an existing owner.
- `KEEP_KNOWLEDGE_PLANE` — retain doctrine/specification as knowledge, not runtime authority.
- `ABSORB` — extract useful capability and retire duplicate ownership.
- `CANDIDATE_WRAP` — promising wrapper capability whose admission is not yet closed.
- `CANDIDATE_ABSORB` — promising donor capability whose extraction is not yet closed.

## 4. Add the projection

Add one `eco:CastleCapabilityProjection` to `ontology/castle-projection.ttl`.

It must contain exactly:

- projected repository;
- source branch;
- source SHA;
- one projected capability;
- disposition;
- projection target;
- runtime placement;
- `CANDIDATE` standing;
- `CONSTRUCT` authority ceiling;
- falsifier;
- projection source.

Do not set `ALIVE`. Do not set `DO`.

## 5. Preserve crown separation

No projected repository may claim either `RUNTIME_CORE` or `CONSEQUENCE_CROWN`.

XaaS remains the runtime crown. CASTLE remains the consequence crown.

## 6. Update the reference projection

Add exactly one row to `docs/castle/reference/capability-matrix.md`.

The repository-local test requires the reference projection to cover the same conservation set as the RDF graph.

## 7. Run the courts

```bash
python3 -m unittest tests.test_castle_projection -v
```

Then evaluate the SPARQL courts over the semantic graph:

- `queries/castle-capability-projection.rq`
- `queries/castle-projection-violations.rq`
- `queries/castle-projection-uniqueness.rq`

The two violation queries must return zero rows.

## 8. Promote only through the receiving owner

A clean projection is still only CANDIDATE.

Promotion belongs to the receiving subsystem's normal path:

```text
projection
 -> owner admission
 -> exact execution
 -> receipt
 -> replay
 -> scoped standing
```

The projection layer itself never promotes a capability to consequential authority.
