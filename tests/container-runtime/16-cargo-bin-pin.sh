#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- '--bin ggen' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract cargo-bin-pin'
