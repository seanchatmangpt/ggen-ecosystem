#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- "grep -m1 '^channel' /tmp/rust-toolchain.toml" "$subject"
printf '%s\n' 'ALIVE container-runtime-contract toolchain-channel-read'
