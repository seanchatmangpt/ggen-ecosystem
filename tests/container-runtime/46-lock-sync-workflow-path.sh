#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'workflow = ".github/workflows/ggen-ecosystem-sync.yml"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-sync-workflow-path'
