#!/usr/bin/env bash
set -eu
grep -Fq -- 'ggen not found on PATH' scripts/doctor.sh
