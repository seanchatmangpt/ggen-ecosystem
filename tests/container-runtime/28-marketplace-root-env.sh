#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'ENV GGEN_MARKETPLACE_ROOT=/opt/ggen-marketplace' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract marketplace-root-env'
