#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen sync run --dry-run --format json-pretty' scripts/doctor.sh
