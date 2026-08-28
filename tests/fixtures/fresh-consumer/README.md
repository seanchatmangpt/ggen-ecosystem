# PR-010 Fresh-Consumer Fixture

## What this is

A minimal, independent consumer project — the "crown test" for the
ggen-ecosystem container. It has ONLY legitimate consumer-side state:

- `ggen.toml` — a manifest a brand-new external repo would write for itself.
  It does not import or reference `vendor/ggen` or `vendor/ggen-marketplace`
  (this repo's own git submodules) by local path — a real external consumer
  has neither checked out. The marketplace pack contract is delivered at the
  container layer instead (see "How this gets run" below).
- `ontology.ttl` — a minimal SHACL shape (`ex:ThingShape` / `ex:Thing`),
  modeled on `~/.claude/skills/run-ggen/smoke.sh`'s verified minimal working
  shape.
- `queries/extract.rq` — a SPARQL `SELECT` with `ORDER BY` (required: ggen's
  `strict_mode` refuses any `SELECT` lacking one, at config-validation time,
  error `E0013`), extracting `?shape ?targetClass ?propPath` from the
  ontology above.
- `templates/hello.tera` — a Tera template iterating `sparql_results`,
  emitting one commented line per query row.

Internal consistency (verified by inspection, since no container exists
locally to run this against yet):

- `ggen.toml`'s `[ontology].source = "ontology.ttl"` matches the file
  actually present in this directory.
- `ggen.toml`'s `[[generation.rules]]` `query.file` and `template.file`
  paths match `queries/extract.rq` and `templates/hello.tera` exactly.
- `extract.rq`'s three projected variables (`?shape`, `?targetClass`,
  `?propPath`) are exactly the three fields `hello.tera` references
  (`row.shape`, `row.targetClass`, `row.propPath`) — no name mismatch.
- `extract.rq`'s WHERE clause (`sh:NodeShape` / `sh:targetClass` /
  `sh:property` / `sh:path`) matches predicates that actually appear in
  `ontology.ttl`'s `ex:ThingShape` individual.
- The TTL syntax mirrors the already-verified-working
  `tests/fixtures/minimal-ggen-project/ontology/data.ttl` shape one-for-one
  (same prefixes, same SHACL pattern), only the namespace and comments
  differ.
- `ORDER BY ?shape ?propPath` is present, satisfying `strict_mode`.

## How this gets run (once a real image exists)

This fixture cannot be exercised yet: `ecosystem.lock.toml`'s `[container]`
section currently has `tag = "UNKNOWN-TODO-not-yet-built"` and
`digest = "UNKNOWN-TODO-not-yet-built"` — no image has been built and pushed
yet. Once PR-004/PR-009 land a real digest, an operator or CI runs:

```bash
docker run --rm \
  -v "$PWD/tests/fixtures/fresh-consumer:/workspace" \
  -w /workspace \
  ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:<digest> \
  ggen sync run
```

Replace `sha256:<digest>` with the real digest recorded in
`ecosystem.lock.toml`'s `[container]` section once it exists. This mounts
ONLY this fixture directory as `/workspace` — no other part of
`ggen-ecosystem` is visible to the container — so a pass here is real
evidence an independent external consumer (with no submodules, no local
`vendor/` tree) can pull the published image and run `ggen sync run`
successfully.

Equivalently, once the composite GitHub Action at
`vendor/ggen-marketplace/packs/github-actions-pack/examples/consume-github-actions-pack/.github/actions/use-ggen-ecosystem`
is wired to the same digest, a consumer repo's own CI workflow can invoke
that action against this fixture directory instead of a raw `docker run`.

For a one-command, one-argument version of the `docker run` invocation
above, see `tests/run-fresh-consumer.sh` in this repo's `tests/` directory
(takes the image ref, e.g. `ghcr.io/seanchatmangpt/ggen-ecosystem@sha256:<digest>`,
as its one argument).

## Expected output

A successful `ggen sync run` writes `out/hello.rs` containing:

```
// PR-010 fresh-consumer crown test output
// shape=https://example.org/fresh-consumer#ThingShape targetClass=https://example.org/fresh-consumer#Thing prop=https://example.org/fresh-consumer#name
```

(one row, since `ontology.ttl` defines exactly one `sh:NodeShape` with one
`sh:property`).
