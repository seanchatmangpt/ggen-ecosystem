#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen --version failed:' scripts/doctor.sh
