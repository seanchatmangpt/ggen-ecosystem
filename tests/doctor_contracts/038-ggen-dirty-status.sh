#!/usr/bin/env bash
set -eu
grep -Fq -- 'git -C vendor/ggen status --short' scripts/doctor.sh
