#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="1-submodules"' scripts/doctor.sh
