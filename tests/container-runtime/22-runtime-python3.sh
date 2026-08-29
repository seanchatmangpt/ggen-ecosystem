#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'python3 bash nodejs' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract runtime-python3'
