#!/usr/bin/env bash
set -eu
grep -Fq -- 'MATCH: all committed .github/workflows/*.yml reported unchanged' scripts/doctor.sh
