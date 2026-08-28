# Admission

Admission converts observations into bounded facts in `O*`; it is not a synonym for discovery.

## Evidence states

- **observed** — directly returned by the relevant source or runtime.
- **verified** — an executable verifier closed the stated predicate on the exact subject.
- **explicitly inferred** — a reversible inference whose basis is recorded.
- **unknown** — not admitted.

## Admission boundaries

Repository presence does not imply ecosystem membership. A candidate profile edge does not imply compatibility. A workflow definition does not imply a successful run. A path in a manifest does not imply the repository is mounted. A file named `receipt` does not imply a verified receipt.

The SHACL shapes in `admission/shapes.ttl`, SPARQL falsifiers in `queries/`, marketplace pack gates, exact dependency locks, and runtime receipts form complementary admission layers; none should be silently substituted for another.
