#!/usr/bin/env bash
# Runs doctor.sh check-1's exact prefix-parsing loop against a SYNTHETIC `git submodule status`
# fixture (not the real vendor/ tree, per the no-touch-vendor constraint) representing:
#   '-' = submodule not initialized at all
#   '+' = submodule checked out but its HEAD does not match the superproject's recorded gitlink SHA
set -u
D="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
status_out="$(cat "$D/submodule-status.txt")"
bad=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  prefix="${line:0:1}"
  if [ "$prefix" = "-" ]; then
    echo "REFUSED[SUBMODULE_NOT_INITIALIZED]:${line#?}"
    bad=1
  elif [ "$prefix" = "+" ]; then
    echo "REFUSED[SUBMODULE_GITLINK_MISMATCH]:${line#?}"
    bad=1
  fi
done <<< "$status_out"
exit $([ "$bad" -eq 1 ] && echo 2 || echo 1)
