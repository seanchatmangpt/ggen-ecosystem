#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen_commit' scripts/doctor.sh
