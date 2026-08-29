#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'COPY --from=builder /out/bin/ggen /usr/local/bin/ggen' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract runtime-ggen-copy'
