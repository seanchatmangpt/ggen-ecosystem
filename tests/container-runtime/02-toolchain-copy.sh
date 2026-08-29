#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'COPY vendor/ggen/rust-toolchain.toml /tmp/rust-toolchain.toml' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract toolchain-copy'
