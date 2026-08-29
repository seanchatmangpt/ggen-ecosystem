#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'digest = "sha256:b9e170233fe15d91003fbfc322786534d208fe8ac1b5c58cc0702d88d9ceeb3c"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-container-digest'
