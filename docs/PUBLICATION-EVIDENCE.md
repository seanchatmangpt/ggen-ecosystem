# Publication evidence classification

Run `just publication-evidence` to evaluate the bounded fixtures under
`tests/publication-evidence/cases/`. This is a read-only `VERIFY` court: it does
not log in to a registry, change package visibility, push an image, or grant
`DO` authority.

## Why the boundary exists

GitHub Actions run `33249382665` built both native platform images and then
failed while pushing each image:

```text
denied: permission_denied: write_package
```

That observation is `REFUSED[PACKAGE_WRITE_PERMISSION]`. It is not
`BUILD_BROKEN`: compilation and image construction reached the registry push
transition. Repair therefore belongs at the package-to-repository Actions
permission boundary, followed by a fresh exact-head run. Re-running the build
without changing that boundary does not add evidence.

## Promotion sequence

A multi-architecture publication reaches `ALIVE[MULTIARCH_PUBLISHED]` only
after all of these observations are present:

1. immutable linux/amd64 child digest;
2. immutable linux/arm64 child digest;
3. immutable OCI image-index digest;
4. successful fresh linux/amd64 consumer;
5. successful fresh linux/arm64 consumer;
6. same-subject replay match.

Tags, cache hits, build success, or a workflow definition cannot substitute for
those observations. A partial platform set remains `PARTIAL_ALIVE`; malformed,
mutable, drifting, unreceipted, or secret-bearing evidence fails closed.

## Recovery routing

- `REFUSED[PACKAGE_WRITE_PERMISSION]`: bind the GHCR package to this repository
  for GitHub Actions writes, then rerun the exact admitted head.
- `BLOCKED[REGISTRY_AUTH]`: repair authentication without publishing secrets.
- `BLOCKED[REGISTRY_*]`: preserve the transport observation and retry only
  after the named condition changes.
- `BUILD_BROKEN[*]`: repair the narrow build cause before another push.
- `UNSUPPORTED[PLATFORM]`: retain the refusal until the capsule admits it.
- `PARTIAL_ALIVE[*]`: execute the missing platform, manifest, consumer, or
  replay edge named by the reason.

The JSON Schema at `schemas/publication-evidence-case.schema.json` defines the
fixture envelope. The Python classifier remains the executable standing court.
