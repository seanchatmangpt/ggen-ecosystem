#!/usr/bin/env bash
set -eu
grep -Fq -- 'IMAGE_NOT_YET_BUILT' scripts/doctor.sh
