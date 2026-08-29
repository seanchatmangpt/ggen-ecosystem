#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'container_workflow = ".github/workflows/ggen-ecosystem-container.yml"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-container-workflow-path'
