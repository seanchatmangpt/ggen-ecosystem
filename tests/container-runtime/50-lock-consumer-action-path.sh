#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'consumer_action = "vendor/ggen-marketplace/packs/github-actions-pack/examples/consume-github-actions-pack/.github/actions/use-ggen-ecosystem"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-consumer-action-path'
