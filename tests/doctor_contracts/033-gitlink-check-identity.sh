#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="7-gitlink-exact"' scripts/doctor.sh
