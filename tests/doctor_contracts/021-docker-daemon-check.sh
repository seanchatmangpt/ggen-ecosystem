#!/usr/bin/env bash
set -eu
grep -Fq -- 'docker info >/dev/null 2>&1' scripts/doctor.sh
