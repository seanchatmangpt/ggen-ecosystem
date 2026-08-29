#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'ggen_marketplace_commit = "89adf4c8476f7edc8067fdbb1c256cfbfa22df6a"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-marketplace-submodule-commit'
