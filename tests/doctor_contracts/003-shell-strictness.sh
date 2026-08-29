#!/usr/bin/env bash
set -eu
grep -Fq -- 'set -u' scripts/doctor.sh
