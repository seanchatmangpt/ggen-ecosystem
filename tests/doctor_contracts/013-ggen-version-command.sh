#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen --version 2>&1' scripts/doctor.sh
