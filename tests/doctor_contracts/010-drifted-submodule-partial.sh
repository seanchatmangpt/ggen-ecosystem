#!/usr/bin/env bash
set -eu
grep -Fq -- 'does not match superproject' scripts/doctor.sh
