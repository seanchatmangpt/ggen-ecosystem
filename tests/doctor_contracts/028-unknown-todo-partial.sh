#!/usr/bin/env bash
set -eu
grep -Fq -- 'documented UNKNOWN-TODO placeholder(s) present' scripts/doctor.sh
