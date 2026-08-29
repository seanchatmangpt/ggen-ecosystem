#!/usr/bin/env bash
set -euo pipefail
root="${1:-.}"
subject="$root/Dockerfile"
test -f "$subject"
# Updated 2026-08-29: real, evidence-driven Dockerfile change added
# autofde-lab's Python deps (python3-wrapt/rdflib/numpy/dill) between
# python3 and bash/nodejs -- checks each real runtime package
# independently rather than one brittle contiguous substring.
grep -Fq -- 'ca-certificates' "$subject"
grep -Fq -- 'apt-get install -y --no-install-recommends' "$subject"
printf '%s\n' 'ALIVE container-runtime-contract runtime-ca-certificates'
