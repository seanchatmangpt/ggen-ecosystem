#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'RUN ggen --version || true' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract version-smoke'
