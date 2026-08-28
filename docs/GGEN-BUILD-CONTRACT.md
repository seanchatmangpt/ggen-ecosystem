# GGen Build Contract

Canonical, verified record of how to build the real `ggen` CLI binary from the
`vendor/ggen` source tree. Written so no future Dockerfile, CI workflow, or
consumer has to rediscover these facts by trial and error — they were each
found the hard way against real `cargo build` output while authoring this
repo's Dockerfile (see `Dockerfile` and
`docs/PRD-ARD-v26.8.28.md` Section 16.1 for where this contract is consumed).

Scope: this document describes `ggen-ecosystem`'s consumption of `vendor/ggen`
as a submodule. It does not modify `vendor/ggen` itself, which is a separate
repository out of scope here.

## The exact build invocation

Run from the root of the `vendor/ggen` checkout (i.e. `WORKDIR` is the ggen
tree itself, not `ggen-ecosystem`):

```bash
cargo build --release --locked --manifest-path crates/ggen-cli/Cargo.toml --bin ggen
```

The built binary is written to `target/release/ggen` (relative to that same
working directory).

## Required system packages

A transitive dependency, `oxrocksdb-sys`, runs `bindgen` against RocksDB's C
API in its `build.rs`. `bindgen` requires a real `libclang` shared library at
build time. Without it, the build fails with:

```text
error: failed to run custom build command for `oxrocksdb-sys ...`
...
Unable to find libclang
```

On Debian/Ubuntu-family images, install before running `cargo build`:

```bash
apt-get update && apt-get install -y --no-install-recommends clang libclang-dev llvm-dev
```

## Three build-topology gotchas, verified against real cargo output

### 1. The package name is `ggen`, not `ggen-cli`

`crates/ggen-cli/Cargo.toml`'s `[package]` section declares `name = "ggen"` —
the crate's package name does not match its directory name (`ggen-cli`).
Selecting the package by name with `-p ggen-cli` fails:

```text
error: package(s) `ggen-cli` not found in workspace
```

(Cargo error text paraphrased from the real observed failure; exact wording
may vary by cargo version — the root cause, a name/directory mismatch, is the
fact that matters.)

### 2. The workspace root `Cargo.toml` ALSO declares `name = "ggen"`

The ggen workspace's root `Cargo.toml` is itself a package with
`name = "ggen"` — the same name as `crates/ggen-cli`. This makes `-p ggen`
ambiguous: cargo resolves it to the root package (which has no `[[bin]]`
target named `ggen`), not to `crates/ggen-cli`, and fails with something like:

```text
error: no bin target named `ggen` in `ggen` package
```

### 3. Disambiguate by `--manifest-path`, not by package name

Because both gotchas above stem from package-name collision/mismatch, the
only reliable selector is the crate's manifest path, not its package name:

```bash
--manifest-path crates/ggen-cli/Cargo.toml --bin ggen
```

This is what the exact build invocation above already does — it is not a
hypothetical alternative, it is the confirmed-working form.

## Toolchain and build-config notes (context, not gotchas)

- Pin the Rust toolchain to whatever `vendor/ggen/rust-toolchain.toml`
  specifies (read its `channel` field), matching vendor/ggen's own CI
  reproducibility guarantee — don't assume a fixed version here, read it from
  the checked-out tree at build time.
- `vendor/ggen/.cargo/config.toml` sets `rustc-wrapper = "sccache"`
  unconditionally. Install `sccache` (`cargo install sccache --locked`) before
  building rather than overriding this repository-level build config.

## See also

- `Dockerfile` (this repo) — the real, working consumer of this contract; its
  inline comments point back here rather than restating this content.
- `docs/PRD-ARD-v26.8.28.md` Section 16.1 ("Builder Stage") — architecture-level
  summary; this document is the canonical detail it points to.
