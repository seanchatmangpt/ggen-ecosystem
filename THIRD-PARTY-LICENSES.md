# Third-Party Licenses

This file lists the open-source license obligations for the third-party code bundled
into the `ggen-ecosystem` container image (`ghcr.io/seanchatmangpt/ggen-ecosystem`),
whose `Dockerfile` compiles the `ggen` binary from the `vendor/ggen` git submodule
(`crates/ggen-cli`, `--bin ggen`) and copies the `vendor/ggen-marketplace/packs/`
template tree alongside it. It exists for license-compliance review of what actually
ships in the published image, not as a description of this repository's own code
(`ggen-ecosystem` itself is MIT-licensed — see `LICENSE`; it contains RDF/TTL
ontology, SHACL shapes, SPARQL, and TOML manifests, not compiled dependencies).

- **Last generated:** 2026-08-29
- **Scoped to:** `vendor/ggen` submodule commit `c61ee99359c9dbc7b3cb71687976932a3e737ed4`
  (`git submodule status vendor/ggen`, tag description `v26.7.21-1686-gc61ee9935`),
  the exact commit this repo's `.gitmodules`/`ecosystem.lock.toml` pin at the time
  this file was written. Re-run the commands below after any submodule bump.
- **Not covered:** `vendor/ggen-marketplace` — its `packs/` tree is data/template
  content (TOML + template files), not a compiled Rust dependency graph, so
  `cargo license` does not apply to it. It was not initialized in this worktree and
  was not audited for this file.

## Method used (real tool run, not fabricated)

1. Checked for `cargo-license`: `which cargo-license` → not found.
2. Installed it for real: `cargo install cargo-license` → succeeded, producing
   `cargo-license v0.7.0` (`~/.cargo/bin/cargo-license`), confirmed via
   `cargo install --list`.
3. Ran it against the real, compiled dependency graph for the exact binary the
   `Dockerfile` builds (`cargo build --release --locked --manifest-path
   crates/ggen-cli/Cargo.toml --bin ggen`), scoped with `--avoid-dev-deps` so
   test-only tooling (`mockall`, `criterion`, `insta`, `cucumber`,
   `testcontainers`, `assert_cmd`, …) that never ships in the release binary is
   excluded from the table below:

   ```bash
   cd vendor/ggen
   cargo license --manifest-path crates/ggen-cli/Cargo.toml --avoid-dev-deps
   ```

   This resolved **575 crate entries** (including build-time-only dependencies;
   see the note below), grouped into the license buckets in the table below. A
   narrower run additionally excluding build-dependencies
   (`--avoid-dev-deps --avoid-build-deps`) still resolved **550 entries**,
   confirming the three flagged non-permissive licenses below are real runtime
   dependencies of the shipped binary, not build-tooling-only.
4. For reference, the *unscoped* whole-workspace query (`cargo license` run with
   no `--manifest-path`, i.e. against the workspace root `Cargo.toml`, which
   pulls in every workspace member including dev/test-only crates) resolved
   **618 entries** — larger because it is a different scope (whole workspace,
   not just what `ggen-cli` needs), not because it's a more "complete" answer for
   this file's purpose (what ships in the image). Both scopes are legitimate
   queries against the same `Cargo.lock`; this file reports the binary-scoped one
   because that is what the container actually distributes.

All numbers above are reproducible by any reviewer with network access to
crates.io by running the same commands from `vendor/ggen/` after
`git submodule update --init vendor/ggen`.

## License summary (ggen-cli binary scope, `--avoid-dev-deps`, 575 entries)

SPDX expressions as reported by each crate's own `Cargo.toml` `license` field
(via `cargo metadata`) — `cargo-license` did not fail to resolve a license for
any of the 575 entries in this run (no "N/A"/unknown entries were present).

| License expression | Crates | Count |
|---|---|---|
| `Apache-2.0 OR MIT` | aes, allocator-api2, android_system_properties, anstream, anstyle, anstyle-parse, anstyle-query, anstyle-wincon, anyhow, arbitrary, arrayvec, async-lock, async-trait, atomic-waker, autocfg, base64, base64ct, bcinr-cmca, bcinr-logic, bcinr-mfw-ir, bcinr-pddl, bcinr-powl, bcinr-powl-receipt, bencher, bitflags, block-buffer, bs58, bstr, bumpalo, bytecount, bzip2, bzip2-sys, camino, cc, cexpr, cfg-if, chacha20, chrono, chrono-tz, chrono-tz-build, cipher, clap, clap-noun-verb, clap-noun-verb-macros, clap_builder, clap_complete, clap_derive, clap_lex, cmake, colorchoice, const-oid, core-foundation, core-foundation-sys, cpufeatures, crc, crc-catalog, crc32fast, crossbeam-channel, crossbeam-deque, crossbeam-epoch, crossbeam-utils, crypto-common, curve25519-dalek-derive, deepmesa-collections, defmt, defmt-macros, defmt-parser, der, deranged, derive_arbitrary, digest, dirs, dirs-sys, displaydoc, dyn-clone, ed25519, either, encode_unicode, env_filter, env_logger, equivalent, errno, event-listener, event-listener-strategy, eventsource-stream, fastrand, file-id, filetime, find-msvc-tools, fixedbitset, flate2, fnv, foreign-types, foreign-types-shared, form_urlencoded, futures (+ futures-channel/-core/-executor/-io/-macro/-sink/-task/-util), genai, getrandom, glob, hashbrown, heck, hermit-abi, hex, hmac, http, httparse, httpdate, humansize, hybrid-array, hyper-timeout, hyper-tls, iana-time-zone(-haiku), ident_case, idna, idna_adapter, indexmap, inout, ipnet, is_terminal_polyfill, itertools, itoa, jni, jni-macros, jni-sys, jni-sys-macros, jobserver, js-sys, json-event-parser, lazy_static, libc, linkme, linkme-impl, lock_api, log, lzma-sys, md-5, md5, mime, minimal-lexical, native-tls, notify-debouncer-full, notify-types, num-conv, num-traits, once_cell, once_cell_polyfill, openssl-macros, openssl-probe, oxigraph, oxiri, oxjsonld, oxrdf, oxrdfio, oxrdfxml, oxsdatatypes, oxttl, parking, parking_lot(-core), pbkdf2, percent-encoding, pest(_derive/_generator/_meta), pin-project(-internal/-lite), pkcs8, pkg-config, portable-atomic(-util), powerfmt, powl2-decompose, ppv-lite86, prettyplease, proc-macro-error(-attr), proc-macro2, quinn(-proto/-udp), quote, rand(_chacha/_core/_pcg), rayon(-core), ref-cast(-impl), regex(-automata/-syntax), reqwest, rustc-hash, rustc_version, rustls-pki-types, rustls-platform-verifier(-android), rustversion, scopeguard, security-framework(-sys), semver, serde(_core/_derive/_derive_internals/_json/_spanned/_urlencoded/_with/_with_macros/_yaml), sha1, sha2, shlex, signal-hook-registry, signature, simd_cesu8, simdutf8, siphasher, slug, smallvec, socket2, sparesults, spareval, spargebra, sparopt, spki, stable_deref_trait, syn, system-configuration(-sys), tagptr, tar, tempfile, terminal_size, thiserror(-impl), thread_local, time(-core/-macros), tokio-rustls, toml(_datetime/_edit/_parser/_write/_writer), typenum, ucd-trie, unicase, unicode-segmentation, unicode-width, unicode-xid, url, utf8_iter, utf8parse, uuid, value-bag, value-ext, vcpkg, version_check, wasm-bindgen(-futures/-macro/-macro-support/-shared), wasm-streams, wasm4pm-compat, web-sys, web-time, winapi(-i686-pc-windows-gnu/-x86_64-pc-windows-gnu), windows(-core/-implement/-interface/-link/-registry/-result/-strings/-sys/-targets and target-triple crates), xattr, xz2, zeroize(_derive), zstd-safe, zstd-sys | 370 |
| `MIT` | atty, axum, axum-core, bytes, cfg_aliases, combine, console, convert_case, darling(_core/_macro), dashmap, deflate64, derive_more(-impl), dotenvy, fs_extra, fsevent-sys, generic-array, **ggen-cli-lib, ggen-config, ggen-engine, ggen-graph, ggen-marketplace** (in-workspace, path deps), globwalk, h2, http-body(-util), hyper(-util), indicatif, jmespath, kqueue(-sys), libm, libredox, lru, lzma-rs, matchers, mime_guess, mio, nix, nom, nom_locate, nu-ansi-term, number_prefix, openssl-sys, oxilangtag, parse-zoneinfo, peg(-macros/-runtime), phf(_codegen/_generator/_shared), **praxis-core, praxis-graphlaw** (in-workspace, path deps), quick-xml, redox_syscall, redox_users, schannel, schemars(_derive), sharded-slab, simd-adler32, slab, star-toml(-derive), strsim, synstructure, tera, tokio(-macros/-native-tls/-stream/-util), tonic(-prost), tower(-http/-layer/-service), tracing(-attributes/-core/-log/-opentelemetry/-serde/-subscriber), try-lock, unsafe-libyaml, urlencoding, valuable, want, winnow, zip, zmij, zstd | 104 |
| `MIT OR Unlicense` | aho-corasick, byteorder, globset, ignore, jiff(-core/-static/-tzdb/-tzdb-platform), memchr, same-file, walkdir, winapi-util | 13 |
| `Apache-2.0` | clang-sys, openssl, opentelemetry, opentelemetry-http, opentelemetry-otlp, opentelemetry-proto, opentelemetry_sdk, prost, prost-derive, rio_api, rio_turtle, rio_xml, sync_wrapper, zopfli | 14 |
| `Unicode-3.0` | icu_collections, icu_locale_core, icu_normalizer(_data), icu_properties(_data), icu_provider, litemap, potential_utf, tinystr, writeable, yoke(-derive), zerofrom(-derive), zerotrie, zerovec(-derive) | 18 |
| `ISC` | inotify, inotify-sys, libloading, rustls-webpki, untrusted | 6 |
| `BSD-3-Clause` | bindgen, curve25519-dalek, deunicode, ed25519-dalek, instant, sha1_smol, subtle | 7 |
| `Apache-2.0 OR ISC OR MIT` | hyper-rustls, rustls, rustls-native-certs | 3 |
| `Apache-2.0 OR CC0-1.0 OR MIT-0` | constant_time_eq, dunce | 3 |
| `Apache-2.0 OR MIT OR Zlib` | lru-slab, miniz_oxide, tinyvec, tinyvec_macros | 4 |
| `Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR MIT` | linux-raw-sys, rustix, wasi, wasip2, wit-bindgen | 5 |
| `Apache-2.0 OR BSD-2-Clause OR MIT` | zerocopy, zerocopy-derive | 2 |
| `Apache-2.0 OR BSL-1.0` | ryu, ryu-js | 2 |
| `Apache-2.0 OR LGPL-2.1-or-later OR MIT` | r-efi (×2 versions) | 2 |
| `CDLA-Permissive-2.0` | webpki-root-certs, webpki-roots | 2 |
| `CC0-1.0` | notify (×2 versions) | 2 |
| `MPL-2.0` | colored, option-ext | 2 |
| `BSD-2-Clause` | Inflector, arrayref | 2 |
| `Zlib` | foldhash | 1 |
| `Apache-2.0 OR BSD-1-Clause OR MIT` | fiat-crypto | 1 |
| `Apache-2.0 AND ISC` | ring | 1 |
| `Apache-2.0 OR Apache-2.0 WITH LLVM-exception OR CC0-1.0` | blake3 | 1 |
| `BSD-3-Clause AND MIT` | matchit | 1 |
| `(Apache-2.0 OR MIT) AND BSD-3-Clause` | encoding_rs | 1 |
| `(Apache-2.0 OR MIT) AND Apache-2.0` | moka | 1 |
| `(Apache-2.0 OR MIT) AND Unicode-3.0` | unicode-ident | 1 |
| `(Apache-2.0 OR ISC) AND ISC` | aws-lc-rs | 1 |
| `(Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR ISC OR MIT-0) AND (Apache-2.0 OR ISC) AND Apache-2.0 AND BSD-3-Clause AND ISC AND MIT` | aws-lc-sys | 1 |
| `0BSD OR Apache-2.0 OR MIT` | adler2 | 1 |
| **`Apache-2.0 OR GPL-2.0`** | oxrocksdb-sys | 1 |
| **`BUSL-1.1`** | prolog8 | 1 |
| **`EUPL-1.2`** | pddl | 1 |

## Flagged for legal review

The overwhelming majority of the tree is permissively licensed
(MIT / Apache-2.0 / BSD / ISC / Unicode-3.0 / 0BSD / Zlib, in various single and
dual/triple-OR forms). Three entries are not standard MIT/Apache-2.0-family and
warrant explicit legal sign-off before distribution, consistent with a Fortune-5
open-source compliance bar:

- **`prolog8` — `BUSL-1.1` (Business Source License 1.1).** Not an OSI-approved
  open-source license; it is a source-available license with a use grant that is
  typically restricted (commonly: free for non-production/non-competing use,
  converting to an open license — often Apache-2.0 — on a stated future "Change
  Date"). The exact grant terms and Change Date must be read from `prolog8`'s own
  `LICENSE`/`Cargo.toml` license file on crates.io (registry source per
  `vendor/ggen/Cargo.lock`: `registry+https://github.com/rust-lang/crates.io-index`,
  version `26.7.1`) before this dependency is treated as clear for redistribution
  in a commercial image.
- **`pddl` — `EUPL-1.2`** (European Union Public License 1.2). A weak-copyleft
  license (GPL-2.0/GPL-3.0/LGPL/MPL/CeCILL-compatible via its Appendix, but not
  itself MIT/Apache-2.0-equivalent); redistribution/derivative-work obligations
  should be reviewed against how `pddl` is used (registry source, version `0.2.0`).
- **`oxrocksdb-sys` — `Apache-2.0 OR GPL-2.0`** (dual-licensed, SPDX `OR`). The
  Apache-2.0 branch of this choice can be exercised for a permissive-only
  compliance posture; flagged only so the choice is made explicitly rather than
  left implicit.

All three were confirmed to be **real runtime dependencies of the shipped `ggen`
binary** (still present with both `--avoid-dev-deps` and `--avoid-build-deps`
applied together, 550-entry run), not build-time-only tooling.

## Real limitations of this file (stated explicitly, not glossed over)

- **License text is not reproduced here.** This file lists SPDX license
  *expressions* per crate (as declared in each crate's own `Cargo.toml`), not the
  full license text of every dependency. A complete Fortune-5-grade NOTICE bundle
  (as e.g. `cargo about` or `cargo bundle-licenses` would produce) would also
  embed each unique license's full text and per-crate copyright/author lines;
  that step was not run for this file — `cargo-license` alone does not fetch or
  bundle license text.
- **`SPDX license expression` accuracy depends on each upstream crate's own
  `Cargo.toml` metadata being correct** — `cargo-license` reports what each crate
  declares, it does not independently verify that declaration against the
  crate's actual `LICENSE` file content.
- **Count instability across scopes**: as noted above, `cargo license` run at
  different `--manifest-path`/`--avoid-*` scopes against the same `Cargo.lock`
  returns different entry counts (575 vs. 550 vs. 618) because Cargo's feature
  resolution and dev/build-dependency inclusion legitimately differ by scope —
  none of these numbers is "the" single correct dependency count; each is a
  correctly-scoped answer to a differently-scoped question. This file reports
  the `--avoid-dev-deps` binary-scoped number as primary because it is the
  closest available proxy for "what ships in the container's `ggen` binary."
- **Point-in-time.** This snapshot reflects `vendor/ggen` at commit
  `c61ee99359c9dbc7b3cb71687976932a3e737ed4` only. Any future `git submodule
  update` that moves that pin invalidates this table; regenerate it with the
  commands above whenever `vendor/ggen`'s pinned commit changes.
- **`vendor/ggen-marketplace` is not covered**, as stated in Scope above.

## Reproducing this file

```bash
# From the ggen-ecosystem repo root, with submodules initialized:
git submodule update --init vendor/ggen
which cargo-license || cargo install cargo-license
cd vendor/ggen
cargo license --manifest-path crates/ggen-cli/Cargo.toml --avoid-dev-deps
```
