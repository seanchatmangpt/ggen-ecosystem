#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="8-dirty-submodules"' scripts/doctor.sh
