# Tutorial: trace one capability into CASTLE

This tutorial follows one remaining capability from source repository to its CASTLE owner without creating a new architectural crown.

We will use MMDIO because its boundary is easy to see: it can deterministically project semantic/planning state into diagrams and presentations, but a diagram must never become semantic authority.

## 1. Find the semantic projection

Open `ontology/castle-projection.ttl` and locate `eco:castle-projection-mmdio`.

The projection records:

- the exact repository head;
- `SemanticDocumentProjection`;
- disposition `CANDIDATE_WRAP`;
- target `seanchatmangpt/ash_surface`;
- runtime placement `POWERLESS_DOCUMENT_PROJECTION`;
- standing `CANDIDATE`;
- authority ceiling `CONSTRUCT`;
- an explicit falsifier.

Nothing in that record says MMDIO owns CASTLE presentation semantics globally.

## 2. Follow the target, not the source

The source capability is useful because it can render a view.

The receiving owner remains the existing CASTLE surface:

```text
CASTLE / XaaS state
       ↓
admitted semantic state
       ↓
MMDIO projection
       ↓
Ash Surface
       ↓
human-readable diagram/presentation
```

The arrow never reverses. Editing the projected presentation does not mutate the semantic source.

## 3. Query the projection

Evaluate `queries/castle-capability-projection.rq` over the ecosystem graph.

The row for MMDIO should show the exact source SHA, target, disposition, runtime placement, CANDIDATE standing, CONSTRUCT ceiling, and falsifier.

Then evaluate:

- `queries/castle-projection-violations.rq`
- `queries/castle-projection-uniqueness.rq`

Both are zero-row courts.

## 4. Understand what would constitute failure

The MMDIO projection is falsified if a diagram, presentation, or Markdown artifact is treated as:

- canonical semantic source;
- runtime authority;
- evidence of execution merely because it rendered successfully.

That is why the projection is useful but non-sovereign.

## 5. Generalize

The same pattern applies to all remaining repositories:

```text
observed source capability
   -> candidate projection
   -> explicit existing owner
   -> owner-specific admission
   -> bounded execution if applicable
   -> receipt/replay
```

This is the purpose of the CASTLE profile: preserve useful capability without multiplying crowns.
