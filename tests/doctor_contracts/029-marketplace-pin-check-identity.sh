#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="6-marketplace-pin"' scripts/doctor.sh
