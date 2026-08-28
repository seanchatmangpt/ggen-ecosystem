#!/usr/bin/env bash
# Adapts doctor.sh check-6 logic (marketplace-pin) to the ggen submodule pin instead,
# pointed at this fixture's ecosystem.lock.toml and the REAL (read-only) vendor/ggen checkout.
set -u
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
FIXTURE_LOCK="tests/fixtures/falsifiers/01-wrong-ggen-commit/ecosystem.lock.toml"
recorded="$(awk -F'"' '/^ggen_commit *=/{print $2; exit}' "$FIXTURE_LOCK")"
actual="$(git -C vendor/ggen rev-parse HEAD 2>&1)"
if [ "$recorded" = "$actual" ]; then
  echo "ALIVE: fixture ggen_commit ($recorded) matches vendor/ggen HEAD -- unexpected for a falsifier fixture"
  exit 1
else
  echo "REFUSED[GGEN_SUBMODULE_DRIFT]:${actual}:${recorded}"
  exit 2
fi
