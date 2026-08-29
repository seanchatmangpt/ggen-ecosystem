#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'COPY vendor/ggen/ /src/' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract ggen-source-copy'
