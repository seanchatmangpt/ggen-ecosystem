#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'FROM debian:bookworm-slim' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract runtime-base'
