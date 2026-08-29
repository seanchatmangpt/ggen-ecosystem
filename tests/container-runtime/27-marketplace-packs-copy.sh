#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'COPY vendor/ggen-marketplace/packs/ /opt/ggen-marketplace/packs/' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract marketplace-packs-copy'
