#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- '--release --locked' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract cargo-locked'
