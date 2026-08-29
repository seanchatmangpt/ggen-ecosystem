#!/usr/bin/env bash
set -eu
grep -Fq -- 'ALIVE | PARTIAL_ALIVE | BLOCKED | BUILD_BROKEN | UNSUPPORTED | UNKNOWN' scripts/doctor.sh
