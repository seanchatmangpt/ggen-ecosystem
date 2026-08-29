#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="2-ggen-binary"' scripts/doctor.sh
