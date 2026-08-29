#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'manifest = "ggen.toml"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-manifest-path'
