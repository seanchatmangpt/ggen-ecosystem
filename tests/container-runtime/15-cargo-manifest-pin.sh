#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- '--manifest-path crates/ggen-cli/Cargo.toml' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract cargo-manifest-pin'
