#!/usr/bin/env bash
set -eu
grep -Fq -- 'exit "$FAIL"' scripts/doctor.sh
