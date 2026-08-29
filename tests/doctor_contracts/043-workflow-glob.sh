#!/usr/bin/env bash
set -eu
grep -Fq -- '.github/workflows/*.yml' scripts/doctor.sh
