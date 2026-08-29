#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'ENV PATH="/usr/local/bin:${PATH}"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract ggen-path-env'
