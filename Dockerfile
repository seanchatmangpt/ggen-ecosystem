# Composed ggen-ecosystem image: a real `ggen` binary built from the vendor/ggen submodule,
# plus the real vendor/ggen-marketplace/packs/ tree, in one image consumers reference by tag or
# digest via GitHub Actions -- replacing curl-a-release-binary consumption. Build requires the
# repo checked out with submodules (`git submodule update --init --recursive` or
# `actions/checkout` with `submodules: recursive`).

# --- builder ------------------------------------------------------------
FROM rustlang/rust:nightly-bookworm AS builder

# Pin the same nightly vendor/ggen's own CI pins (rust-toolchain.toml), so this build matches
# the toolchain vendor/ggen's own reproducibility guarantee assumes.
COPY vendor/ggen/rust-toolchain.toml /tmp/rust-toolchain.toml
RUN TOOLCHAIN=$(grep -m1 '^channel' /tmp/rust-toolchain.toml | sed -E 's/.*"(.*)".*/\1/') \
    && rustup toolchain install "$TOOLCHAIN" --profile minimal --component rustfmt --component clippy \
    && rustup default "$TOOLCHAIN"

# vendor/ggen/.cargo/config.toml sets `rustc-wrapper = "sccache"` unconditionally -- install it
# rather than fight the repo's own build config (matches the real pattern already proven in
# vendor/ggen/.github/actions/setup-ggen-build/action.yml, which does the same via
# taiki-e/install-action in CI).
RUN cargo install sccache --locked

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
RUN cargo build --release --locked --manifest-path crates/ggen-cli/Cargo.toml --bin ggen

RUN mkdir -p /out/bin \
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
    && apt-get install -y --no-install-recommends ca-certificates git python3 bash nodejs \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /out/bin/ggen /usr/local/bin/ggen
COPY vendor/ggen-marketplace/packs/ /opt/ggen-marketplace/packs/

ENV GGEN_MARKETPLACE_ROOT=/opt/ggen-marketplace
ENV PATH="/usr/local/bin:${PATH}"

RUN ggen --version || true

ENTRYPOINT []
CMD ["ggen", "--help"]
