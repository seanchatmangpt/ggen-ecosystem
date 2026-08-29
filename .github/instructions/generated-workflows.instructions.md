---
applyTo: ".github/workflows/ggen-ecosystem-*.yml"
---

These files are GGen-manufactured projections. Review them for security, permissions, syntax, and behavioral defects, but do not repair them by direct editing.

When a defect is found:
1. identify the corresponding semantic fact in `ontology.ttl` or the admitted Marketplace template/source;
2. preserve the failing evidence;
3. repair the semantic producer source;
4. execute the repository's real GGen regeneration path;
5. verify that the generated diff is the deterministic consequence of that source change.

A hand-edited generated workflow is `REFUSED[GENERATED_OUTPUT_DRIFT]` regardless of whether the YAML appears correct.
