#!/usr/bin/env bash
set -eu
grep -Fq -- 'not present in dry-run decisions' scripts/doctor.sh
