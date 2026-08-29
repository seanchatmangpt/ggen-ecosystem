#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen sync run --dry-run 2>/tmp/doctor_dry2_err.$$' scripts/doctor.sh
