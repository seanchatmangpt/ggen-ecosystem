#!/usr/bin/env bash
# Adapts doctor.sh check-6 (marketplace-pin) logic verbatim, pointed at this fixture's
# ecosystem.lock.toml, compared against the REAL (untouched, read-only) vendor/ggen-marketplace.
set -u
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
FIXTURE_LOCK="tests/fixtures/falsifiers/02-wrong-marketplace-commit/ecosystem.lock.toml"
recorded="$(awk -F'"' '/ggen_marketplace_commit *=/{print $2; exit}' "$FIXTURE_LOCK")"
actual="$(git -C vendor/ggen-marketplace rev-parse HEAD 2>&1)"
if [ "$recorded" = "$actual" ]; then
  echo "ALIVE: unexpected match -- fixture is supposed to be wrong"
  exit 1
else
  echo "REFUSED[MARKETPLACE_SUBMODULE_DRIFT]:${actual}:${recorded}"
  exit 2
fi
