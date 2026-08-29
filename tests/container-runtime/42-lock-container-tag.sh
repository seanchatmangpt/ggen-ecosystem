#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'tag = "v26.8.28"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-container-tag'
