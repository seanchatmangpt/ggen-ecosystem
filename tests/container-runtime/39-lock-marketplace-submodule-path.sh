#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'ggen_marketplace_path = "vendor/ggen-marketplace"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-marketplace-submodule-path'
