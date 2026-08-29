#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="11-image-presence"' scripts/doctor.sh
