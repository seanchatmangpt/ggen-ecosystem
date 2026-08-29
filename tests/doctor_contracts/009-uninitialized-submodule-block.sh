#!/usr/bin/env bash
set -eu
grep -Fq -- 'not initialized: ${line#?}' scripts/doctor.sh
