#!/usr/bin/env bash
set -eu
grep -Fq -- 'FM-PACK-008' scripts/doctor.sh
