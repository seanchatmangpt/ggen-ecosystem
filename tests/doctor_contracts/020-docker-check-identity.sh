#!/usr/bin/env bash
set -eu
grep -Fq -- 'name="4-docker-image"' scripts/doctor.sh
