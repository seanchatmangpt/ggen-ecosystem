# Composed ggen-ecosystem image: a real `ggen` binary built from the vendor/ggen submodule,
# plus the real vendor/ggen-marketplace/packs/ tree, AutoFDE sources, and the pinned beam4pm
# submodule in one image consumers reference by tag or digest via GitHub Actions. Build requires
# the repo checked out with submodules (`git submodule update --init --recursive` or
# `actions/checkout` with `submodules: recursive`).

# --- builder ------------------------------------------------------------
FROM rustlang/rust:nightly-bookworm AS builder

# Pin the same nightly vendor/ggen's own CI pins (rust-toolchain.toml), so this build matches
# the toolchain vendor/ggen's own reproducibility guarantee assumes.
#
# Deliberately NOT a cache mount: this layer's only real input is
# rust-toolchain.toml (rarely changes), so regular Docker layer caching
# (via cache-from/cache-to: type=gha on the workflow's build-push step,
# added below) already gives a full skip on an unchanged pin -- no
# --mount=type=cache needed. A cache mount here would actually BREAK the
# build: content written under a cache-mounted RUSTUP_HOME is invisible to
# every later RUN instruction (cache mounts are scoped to one instruction,
# not part of the persisted image layer), so the very next step (cargo
# install sccache) would find no toolchain installed. Caught and reverted
# in-session before ever being built.
COPY vendor/ggen/rust-toolchain.toml /tmp/rust-toolchain.toml
RUN TOOLCHAIN=$(grep -m1 '^channel' /tmp/rust-toolchain.toml | sed -E 's/.*"(.*)".*/\1/') \
    && rustup toolchain install "$TOOLCHAIN" --profile minimal --component rustfmt --component clippy \
    && rustup default "$TOOLCHAIN"

# vendor/ggen/.cargo/config.toml sets `rustc-wrapper = "sccache"` unconditionally -- install it
# rather than fight the repo's own build config (matches the real pattern already proven in
# vendor/ggen/.github/actions/setup-ggen-build/action.yml, which does the same via
# taiki-e/install-action in CI).
#
# Real caching fix (2026-08-29): BuildKit cache mounts for cargo's registry and sccache's own
# cache dir. Explicit SCCACHE_DIR=/sccache avoids the documented $HOME-doesn't-expand-in-Cargo's
# [env] table bug (see the .cargo/config.toml comment this repeats) AND gives a fixed, known
# mount target. Combined with cache-from/cache-to: type=gha on the container workflow's
# build-push steps (the mechanism that actually persists across separate GitHub-hosted-runner
# VMs -- a local mount alone does not survive between independent workflow runs).
ENV SCCACHE_DIR=/sccache
RUN --mount=type=cache,target=/usr/local/cargo/registry,sharing=locked \
    --mount=type=cache,target=/sccache,sharing=locked \
    cargo install sccache --locked

# The workspace pulls in oxrocksdb-sys, whose build.rs runs bindgen against RocksDB's C API --
# bindgen needs a real libclang shared library at build time (confirmed the hard way: without
# this, cargo build fails with "Unable to find libclang" from bindgen-0.72.1, not guessed).
RUN apt-get update \
    && apt-get install -y --no-install-recommends clang libclang-dev llvm-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY vendor/ggen/ /src/

# Two real, confirmed gotchas here, both found the hard way against real cargo output:
# (1) crates/ggen-cli/Cargo.toml's [package] name is "ggen", not "ggen-cli" (the dir name) --
#     `-p ggen-cli` fails with "did not match any packages".
# (2) the workspace ROOT Cargo.toml ALSO declares `name = "ggen"` -- a duplicate package name --
#     so `-p ggen` resolves ambiguously to the root package (which has no [[bin]] named ggen:
#     "no bin target named `ggen` in `ggen` package"), not crates/ggen-cli. Disambiguate by
#     manifest path instead of package name.
#
# Real caching fix (2026-08-29): --mount=type=cache for cargo's registry (downloaded crate
# sources/index), sccache's own compiled-object cache, and cargo's target/ build dir itself
# (incremental build artifacts) -- this is the actual expensive step (the whole ggen workspace,
# minutes of compilation from cold). The final `cp` MUST happen inside this same RUN: content
# written to a --mount=type=cache target is only visible within the instruction that mounted it,
# never in the resulting image layer or any later RUN step -- verified against real BuildKit
# cache-mount semantics before relying on it, after almost making exactly this mistake for the
# rustup toolchain layer above (caught and reverted before ever being built).
RUN --mount=type=cache,target=/usr/local/cargo/registry,sharing=locked \
    --mount=type=cache,target=/sccache,sharing=locked \
    --mount=type=cache,target=/src/target,sharing=locked \
    cargo build --release --locked --manifest-path crates/ggen-cli/Cargo.toml --bin ggen \
    && mkdir -p /out/bin \
    && cp "$(find /src/target/release -maxdepth 1 -type f -name ggen)" /out/bin/ggen

# --- final ---------------------------------------------------------------
FROM debian:bookworm-slim

# git + python3 are real runtime requirements of the ggen-ecosystem-sync.yml steps that now run
# inside this container (git rev-parse for submodule-drift checks, python3 for the pack-admission
# and receipt-binding inline scripts) -- not speculative, confirmed against ontology.ttl's real
# ex:admit/ex:evidence step gha:runCommand facts.
#
# bash is a real runtime requirement, found via `act` simulating a real GH Actions run against
# this exact image: several generated `gha:runCommand` steps use `set -o pipefail` and
# `[[ ... ]]`, neither supported by Debian's default /bin/sh (dash) -- confirmed via
# `act workflow_dispatch -j construct` ("set: Illegal option -o pipefail", "[[: not found").
# This is a real production defect, not act-specific: GitHub's documented shell-selection
# fallback uses `sh` for a container job's `run:` steps when the container has no `bash` on
# PATH, so a real GitHub-hosted runner would hit the identical failure against this image.
#
# nodejs was also added during local `act` testing to unblock actions/checkout inside the
# container, but per GitHub's actions/runner docs a real hosted runner injects a glibc Node
# binary via a bind-mounted /__e/ directory regardless of the image -- this debian (glibc)
# image would already work on real GitHub without it. Installing nodejs here anyway is
# harmless (small apt package, matches local `act` runs to production behavior) but is NOT
# claimed as fixing a real GitHub-side defect the way bash is.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git python3 python3-wrapt python3-rdflib python3-numpy python3-dill bash nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /out/bin/ggen /usr/local/bin/ggen
COPY vendor/ggen-marketplace/packs/ /opt/ggen-marketplace/packs/
COPY vendor/autofde-lab/src/ /opt/autofde-lab/src/
COPY vendor/beam4pm/ /opt/beam4pm/

ENV GGEN_MARKETPLACE_ROOT=/opt/ggen-marketplace
ENV BEAM4PM_ROOT=/opt/beam4pm
ENV PYTHONPATH="/opt/autofde-lab/src"
ENV PATH="/usr/local/bin:${PATH}"

# Fail the image build if the pinned beam4pm submodule was not initialized into the build context.
RUN test -f "$BEAM4PM_ROOT/mix.exs" \
    && test -f "$BEAM4PM_ROOT/rebar.config" \
    && test -d "$BEAM4PM_ROOT/native"

RUN ggen --version || true

ENTRYPOINT []
CMD ["ggen", "--help"]
