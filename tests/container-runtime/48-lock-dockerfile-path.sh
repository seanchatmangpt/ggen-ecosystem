#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'dockerfile = "Dockerfile"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-dockerfile-path'
