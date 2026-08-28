#!/usr/bin/env bash
# Adapts doctor.sh check-6's directory-existence guard, pointed at this fixture root
# (which deliberately has no vendor/ggen-marketplace directory at all).
set -u
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$D/fixture-root"
if [ ! -f ecosystem.lock.toml ]; then
  echo "UNKNOWN: ecosystem.lock.toml not found"; exit 1
elif [ ! -d vendor/ggen-marketplace ]; then
  echo "REFUSED[MARKETPLACE_SUBMODULE_MISSING]:vendor/ggen-marketplace"
  exit 2
else
  echo "ALIVE: unexpected -- marketplace directory present"
  exit 1
fi
