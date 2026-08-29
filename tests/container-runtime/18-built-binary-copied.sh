#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- '/out/bin/ggen' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract built-binary-copied'
