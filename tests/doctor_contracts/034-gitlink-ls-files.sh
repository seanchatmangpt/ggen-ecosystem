#!/usr/bin/env bash
set -eu
grep -Fq -- 'git ls-files -s vendor/ggen vendor/ggen-marketplace' scripts/doctor.sh
