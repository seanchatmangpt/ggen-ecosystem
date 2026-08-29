#!/usr/bin/env bash
set -eu
grep -Fq -- 'Exit code: 0 if no check emitted BLOCKED/BUILD_BROKEN/UNKNOWN, else 1.' scripts/doctor.sh
