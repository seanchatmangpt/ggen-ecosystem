#!/usr/bin/env bash
set -eu
grep -Fq -- 'prefix="${line:0:1}"' scripts/doctor.sh
