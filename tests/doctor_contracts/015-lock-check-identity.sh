#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="3-lock-hash-match"' scripts/doctor.sh
