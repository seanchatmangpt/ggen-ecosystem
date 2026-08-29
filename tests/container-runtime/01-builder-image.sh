#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
grep -Fq -- 'FROM rustlang/rust:nightly-bookworm AS builder' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract builder-image'
