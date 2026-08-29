#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/ecosystem.lock.toml"
test -f "$subject"
grep -Fq -- 'commit_sha = "c61ee99359c9dbc7b3cb71687976932a3e737ed4"' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract lock-ggen-commit'
