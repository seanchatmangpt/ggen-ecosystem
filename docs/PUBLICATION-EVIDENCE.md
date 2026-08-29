# Publication evidence classification

Use `just publication-evidence` to evaluate the bounded GHCR/OCI publication fixtures under `tests/publication-evidence/cases/`. Use `just publication-evidence-test` for the full self-test + exact 52-case conformance court.

This is a read-only `VERIFY` court. It does not log in to a registry, change package visibility, push an image, release a package, or grant `DO` authority.

## Why this boundary exists

A real GitHub Actions publication attempt built both native platform images and reached the registry push transition, then returned:

```text
denied: permission_denied: write_package
```

That observation is `REFUSED[PACKAGE_WRITE_PERMISSION]`, not `BUILD_BROKEN`: compilation and image construction had already succeeded. The lawful repair belongs at the package-to-repository Actions permission boundary; repeating the build without changing that authority boundary adds no new evidence.

## Promotion sequence

A multi-architecture publication reaches `ALIVE[MULTIARCH_PUBLISHED]` only after all of these observations exist for the same admitted subject:

1. immutable `linux/amd64` child digest;
2. immutable `linux/arm64` child digest;
3. immutable OCI image-index digest;
4. successful fresh `linux/amd64` consumer;
5. successful fresh `linux/arm64` consumer;
6. replay consequence match.

Tags, cache hits, build success, or a workflow definition cannot substitute for those observations. A partial platform set remains `PARTIAL_ALIVE`; malformed, mutable, drifting, unreceipted, secret-bearing, or authority-violating evidence fails closed.

## Recovery routing

- `REFUSED[PACKAGE_WRITE_PERMISSION]`: bind the GHCR package to the repository for authorized Actions writes, then rerun the exact admitted head.
- `BLOCKED[REGISTRY_AUTH]`: repair authentication without publishing secrets.
- `BLOCKED[REGISTRY_*]`: preserve the transport observation and retry only after the named condition changes.
- `BUILD_BROKEN[*]`: repair the narrow build cause before another publication attempt.
- `UNSUPPORTED[PLATFORM]`: retain the unsupported standing until the capsule admits it.
- `PARTIAL_ALIVE[*]`: execute the missing platform, manifest, consumer, or replay edge named by the reason.

## Conformance contract

`schemas/publication-evidence-case.schema.json` defines the fixture envelope. The executable classifier validates the same required fields, standing vocabulary, `VERIFY` authority ceiling, `publication.*` acceptance-edge namespace, reason syntax, and uniqueness of case IDs and semantic fingerprints before it accepts the behavioral result.

The stale draft that introduced this court contained an over-escaped schema regex (`^publication\\\\.` in JSON source). That pattern represented a literal backslash rather than the intended dot separator. The current contract uses `^publication\\.` and the executable validator independently requires `acceptance_edge.startswith("publication.")` so this defect is falsifiable in CI.
