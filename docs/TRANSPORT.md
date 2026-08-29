# Transport

Transport answers how an exact admitted object becomes executable without changing identity.

The intended primary transport is a composed `ggen-ecosystem` container image: `Dockerfile` builds a real `ggen` binary from the `vendor/ggen` submodule and copies the `vendor/ggen-marketplace/packs/` tree (plus `vendor/autofde-lab/src/`) into a `debian:bookworm-slim` runtime image, published to `ghcr.io/seanchatmangpt/ggen-ecosystem`. `.github/workflows/ggen-ecosystem-container.yml` builds and publishes it as three jobs — `build-amd64` and `build-arm64` each push a single-arch image tagged `<tag>-amd64`/`<tag>-arm64`, then `merge-manifest` (which `needs: [build-arm64, build-amd64]`) runs `docker buildx imagetools create` to fuse them into one multi-arch manifest published as both `<tag>` and `latest`. `.github/workflows/ggen-ecosystem-sync.yml` then runs its steps `container:`-scoped inside that pinned image rather than installing a `ggen` binary directly on the runner, and the composite action at `vendor/ggen-marketplace/packs/github-actions-pack/examples/consume-github-actions-pack/.github/actions/use-ggen-ecosystem/action.yml` lets consumer repos `docker run` that same published image against their own `ggen.toml` without installing `ggen` locally. This supersedes the earlier binary-release-consumption path: `ecosystem.lock.toml`'s `[release]` section is kept only as the source-identity record binding `vendor/ggen`'s vendored commit, not as an active transport.

`ecosystem.lock.toml`'s `[container]` section is the exact record of this transport's current standing — check it before trusting the digest is pullable: as of the last recorded observation, a hosted-run replay (Actions run `33238309149`) hit `manifest unknown` pulling the pinned digest during job-container initialization, so the section's `standing = "BLOCKED"` and `requires_republish = true` until a fresh publish, pull, and consumer execution are observed.

Other reversible lawful transports remain available:
1. already-present exact sibling checkout (e.g. the `vendor/ggen`, `vendor/ggen-marketplace`, `vendor/autofde-lab` submodule checkouts themselves);
2. exact-SHA archive/materialization;
3. clone/fetch to exact SHA;
4. workflow artifact carrying the exact tree;
5. dependency-closed reconstruction when full history is unnecessary.

Transport failure changes topology; it does not revoke other lawful edges. A connector repository object is not a mounted checkout, and a checkout at the wrong SHA is not the admitted subject.
