#!/usr/bin/env bash
set -eu
grep -Fq -- 'BLOCKED|BUILD_BROKEN|UNKNOWN) FAIL=1' scripts/doctor.sh
