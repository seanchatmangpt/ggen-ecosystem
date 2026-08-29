#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'clang libclang-dev llvm-dev' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract builder-clang'
