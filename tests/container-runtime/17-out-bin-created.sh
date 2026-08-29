#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'mkdir -p /out/bin' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract out-bin-created'
