#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'release = "v26.8.28"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-ggen-release'
