#!/usr/bin/env bash
# Host-level ANALOG of doctor.sh check-2 (ggen-binary), run with a PATH that deliberately
# excludes ggen -- a real, runnable stand-in for "the image's ggen executable marker is
# missing", since we may not build/run a container in this task.
set -u
if ! PATH="/usr/bin:/bin" command -v ggen >/dev/null 2>&1; then
  echo "REFUSED[GGEN_EXECUTABLE_NOT_FOUND]:PATH=/usr/bin:/bin"
  exit 2
else
  echo "ALIVE: unexpected -- ggen found on restricted PATH"
  exit 1
fi
