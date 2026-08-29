#!/usr/bin/env bash
set -eu
grep -Fq -- 'ghcr.io/seanchatmangpt/ggen-ecosystem' scripts/doctor.sh
