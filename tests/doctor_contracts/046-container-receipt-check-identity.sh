#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="10-container-receipt"' scripts/doctor.sh
