#!/usr/bin/env bash
set -eu
grep -Fq -- 'git submodule status 2>&1' scripts/doctor.sh
