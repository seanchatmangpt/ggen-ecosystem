#!/usr/bin/env bash
set -eu
grep -Fq -- 'git -C vendor/ggen-marketplace status --short' scripts/doctor.sh
