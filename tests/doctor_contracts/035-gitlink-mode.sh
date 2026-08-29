#!/usr/bin/env bash
set -eu
grep -Fq -- 'expected 160000' scripts/doctor.sh
