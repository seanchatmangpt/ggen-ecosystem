#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
# Updated 2026-08-29 -- see 20-runtime-ca-certificates.sh for why.
grep -Fq -- ' python3 ' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract runtime-python3'
