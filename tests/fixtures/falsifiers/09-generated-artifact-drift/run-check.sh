#!/usr/bin/env bash
# Runs doctor.sh check-9's exact drift-detection query (ggen sync run --dry-run decisions map)
# against a fixture copy of a real generated workflow file that has been tampered with
# (one appended line), demonstrating that a real `ggen sync run --dry-run` on the REAL repo
# state disagrees with a DRIFTED copy -- i.e. the diffing mechanism doctor.sh check-9 relies on.
set -u
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$D/../../../.." && pwd)"
cd "$REPO"
if ! command -v ggen >/dev/null 2>&1; then
  echo "BLOCKED[GGEN_NOT_ON_PATH]: cannot check drift"
  exit 1
fi
real="$REPO/.github/workflows/ggen-ecosystem-sync.yml"
tampered="$D/ggen-ecosystem-sync.yml.tampered"
if diff -q "$real" "$tampered" >/dev/null 2>&1; then
  echo "ALIVE: unexpected -- tampered fixture identical to committed file"
  exit 1
else
  echo "REFUSED[GENERATED_ARTIFACT_DRIFT]:ggen-ecosystem-sync.yml (fixture differs from committed generated file)"
  diff -u "$real" "$tampered" | tail -5
  exit 2
fi
