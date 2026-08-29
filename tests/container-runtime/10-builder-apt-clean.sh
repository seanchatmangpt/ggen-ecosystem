#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'rm -rf /var/lib/apt/lists/*' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract builder-apt-clean'
