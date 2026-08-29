#!/usr/bin/env bash
set -eu
grep -Fq -- 'FAIL=0' scripts/doctor.sh
