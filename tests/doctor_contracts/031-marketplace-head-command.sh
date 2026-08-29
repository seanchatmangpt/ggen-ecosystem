#!/usr/bin/env bash
set -eu
grep -Fq -- 'git -C vendor/ggen-marketplace rev-parse HEAD' scripts/doctor.sh
