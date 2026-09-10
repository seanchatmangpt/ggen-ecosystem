# Composed ggen-ecosystem image: a real `ggen` binary built from the vendor/ggen submodule,
# plus the real vendor/ggen-marketplace/packs/ tree, AutoFDE sources, and the pinned beam4pm
# submodule in one image consumers reference by tag or digest via GitHub Actions. Build requires
# the repo checked out with submodules (`git submodule update --init --recursive` or
# `actions/checkout` with `submodules: recursive`).

# --- builder ------------------------------------------------------------
FROM rustlang/rust:nightly-bookworm AS builder

# Pin the same nightly vendor/ggen's own CI pins (rust-toolchain.toml), so this build matches
# the toolchain vendor/ggen's own reproducibility guarantee assumes.
COPY vendor/ggen/rust-toolchain.toml /tmp/rust-toolchain.toml
RUN TOOLCHAIN=$(grep -m1 '^channel' /tmp/rust-toolchain.toml | sed -E 's/.*"(.*)".*/\1/') \
    && rustup toolchain install "$TOOLCHAIN" --profile minimal --component rustfmt --component clippy \
    && rustup default "$TOOLCHAIN"

# vendor/ggen/.cargo/config.toml sets `rustc-wrapper = "sccache"` unconditionally.
ENV SCCACHE_DIR=/sccache
RUN --mount=type=cache,target=/usr/local/cargo/registry,sharing=locked \
    --mount=type=cache,target=/sccache,sharing=locked \
    cargo install sccache --locked

# oxrocksdb-sys build.rs runs bindgen and therefore requires libclang.
RUN apt-get update \
    && apt-get install -y --no-install-recommends clang libclang-dev llvm-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY vendor/ggen/ /src/

# Build the real CLI from its unambiguous manifest path. Cache mounts are build-only;
# copy the resulting binary out in this same instruction so it reaches the final image.
RUN --mount=type=cache,target=/usr/local/cargo/registry,sharing=locked \
    --mount=type=cache,target=/sccache,sharing=locked \
    --mount=type=cache,target=/src/target,sharing=locked \
    cargo build --release --locked --manifest-path crates/ggen-cli/Cargo.toml --bin ggen \
    && mkdir -p /out/bin \
    && cp "$(find /src/target/release -maxdepth 1 -type f -name ggen)" /out/bin/ggen

# --- final ---------------------------------------------------------------
FROM debian:bookworm-slim

# Runtime dependencies used by generated sync steps and composed AutoFDE/beam4pm surfaces.
# AutoFDE's own pyproject requires wrapt>=2.2.1 because core.Constraint intentionally uses
# wrapt.lru_cache (the per-instance method-cache API introduced in wrapt 2.2). Debian
# bookworm's python3-wrapt predates that API, so install the exact admitted minimum in an
# isolated venv while retaining Debian's rdflib/numpy/dill through --system-site-packages.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git python3 python3-venv python3-rdflib python3-numpy python3-dill bash nodejs \
    && python3 -m venv --system-site-packages /opt/ggen-python \
    && /opt/ggen-python/bin/pip install --no-cache-dir 'wrapt==2.2.1' \
    && /opt/ggen-python/bin/python -c 'import wrapt; assert hasattr(wrapt, "lru_cache")' \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /out/bin/ggen /usr/local/bin/ggen
COPY vendor/ggen-marketplace/packs/ /opt/ggen-marketplace/packs/
COPY vendor/autofde-lab/src/ /opt/autofde-lab/src/
COPY vendor/beam4pm/ /opt/beam4pm/

ENV GGEN_MARKETPLACE_ROOT=/opt/ggen-marketplace
ENV BEAM4PM_ROOT=/opt/beam4pm
ENV PYTHONPATH="/opt/autofde-lab/src"
ENV PATH="/opt/ggen-python/bin:/usr/local/bin:${PATH}"

# Fail the image build if required composed surfaces are absent.
RUN test -f "$BEAM4PM_ROOT/mix.exs" \
    && test -f "$BEAM4PM_ROOT/rebar.config" \
    && test -d "$BEAM4PM_ROOT/native" \
    && python3 -c 'import wrapt; assert hasattr(wrapt, "lru_cache")'

RUN ggen --version

ENTRYPOINT []
CMD ["ggen", "--help"]
